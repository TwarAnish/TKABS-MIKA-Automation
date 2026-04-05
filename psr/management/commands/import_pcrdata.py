import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.conf import settings

from psr.models import PCRData

class Command(BaseCommand):
    help = "Import raw PCR data from .xls/.xlsx file into PCRData dump table"

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            type=str,
            help="Filename (e.g., 'PCR_Dump.xlsx') or full path"
        )
        parser.add_argument('--dry-run', action='store_true', help="Show what would be imported without saving")

    def handle(self, *args, **options):
        filename_or_path = options['file']
        dry_run = options['dry_run']

        # Resolve file path
        if os.path.isabs(filename_or_path):
            file_path = filename_or_path
        else:
            file_path = os.path.join(settings.BASE_DIR, filename_or_path)

        if not os.path.isfile(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        self.stdout.write(f"Importing PCR data: {os.path.basename(file_path)}")

        # 1. Read Excel
        df = None
        for engine in ['openpyxl', 'xlrd']:
            try:
                df = pd.read_excel(
                    file_path,
                    sheet_name="Sheet1",
                    skiprows=2,
                    engine=engine
                )
                break
            except Exception as e:
                self.stdout.write(f"Engine {engine} failed: {e}")

        if df is None or df.empty:
            self.stderr.write(self.style.ERROR("Could not read the Excel file or sheet is empty."))
            return

        # 2. Required columns mapping
        required_cols = [
            'PCR No', 'P.O.No.', 'C.O.No.', 'Name', 
            'Item Cd', 'Description', 'Rate', 'PCR.Date', 'Rcpt.Qt'
        ]
        
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            self.stderr.write(self.style.ERROR(f"Missing required columns: {missing}"))
            return

        # 3. Clean and Filter
        # Extract only relevant columns to avoid key errors later
        df = df[required_cols].copy()
        
        # Drop rows where critical identifiers (CO No or PCR No) are missing
        df.dropna(subset=['C.O.No.', 'PCR No'], inplace=True)
        
        # Clean Strings
        df['C.O.No.'] = df['C.O.No.'].astype(str).str.strip()
        df['PCR No'] = df['PCR No'].astype(str).str.strip()
        
        # Numeric conversion for Rate and Quantity
        df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce').fillna(0)
        df['Rcpt.Qt'] = pd.to_numeric(df['Rcpt.Qt'], errors='coerce').fillna(0)
        
        # Date conversion
        df['PCR.Date'] = pd.to_datetime(df['PCR.Date'], errors='coerce')

        valid_count = len(df)
        self.stdout.write(f"Found {valid_count} valid rows after cleaning.")

        if valid_count == 0:
            self.stdout.write(self.style.WARNING("No valid data to import."))
            return

        # 4. Prepare objects
        entries = []
        for _, row in df.iterrows():
            entries.append(PCRData(
                co_no=row['C.O.No.'],
                pcr_no=row['PCR No'],
                po_no=str(row['P.O.No.']).strip() if pd.notna(row['P.O.No.']) else "",
                pcr_date=row['PCR.Date'] if pd.notna(row['PCR.Date']) else None,
                item_code=str(row['Item Cd']).strip(),
                description=str(row['Description']).strip(),
                supplier_name=str(row['Name']).strip(),
                rate=row['Rate'],
                recp_qty=row['Rcpt.Qt']
            ))

        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"[DRY RUN] Would import {len(entries)} records."))
            return

        # 5. Bulk import
        start_time = timezone.now()

        with transaction.atomic():
            # Standard practice for 'dump' tables: Clear old, bring in new
            deleted_count, _ = PCRData.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing PCRData records."))

            batch_size = 5000
            for i in range(0, len(entries), batch_size):
                batch = entries[i:i + batch_size]
                PCRData.objects.bulk_create(batch)

        duration = (timezone.now() - start_time).total_seconds()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {len(entries)} PCRData records in {duration:.2f}s"
            )
        )