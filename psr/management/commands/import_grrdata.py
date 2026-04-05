import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.conf import settings

from psr.models import GRRData

class Command(BaseCommand):
    help = "Import raw GRR data from .xls/.xlsx file into GRRData dump table"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help="Filename or full path")
        parser.add_argument('--dry-run', action='store_true', help="Show counts without saving")

    def handle(self, *args, **options):
        filename_or_path = options['file']
        dry_run = options['dry_run']

        file_path = filename_or_path if os.path.isabs(filename_or_path) else os.path.join(settings.BASE_DIR, filename_or_path)

        if not os.path.isfile(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        # 1. Read Excel
        df = None
        for engine in ['openpyxl', 'xlrd']:
            try:
                df = pd.read_excel(file_path, sheet_name="Sheet1", skiprows=2, engine=engine)
                break
            except Exception as e:
                self.stdout.write(f"Engine {engine} failed: {e}")

        if df is None or df.empty:
            self.stderr.write(self.style.ERROR("Could not read data from 'Sheet1'."))
            return

        # 2. Required columns from your new specs
        required_cols = ['P.O.No.', 'GRR#', 'Item Cd', 'Description', 'Name', 'C.O.No.', 'GRR.Date', 'Rate', 'RcvdQty-SU']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            self.stderr.write(self.style.ERROR(f"Missing required columns: {missing}"))
            return

        # 3. Clean and Filter
        # Remove rows where critical identifiers are missing
        df = df.dropna(subset=['C.O.No.', 'GRR#']).copy()
        
        # Numeric conversions
        df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce').fillna(0)
        df['RcvdQty-SU'] = pd.to_numeric(df['RcvdQty-SU'], errors='coerce').fillna(0)
        
        # String cleaning
        df['C.O.No.'] = df['C.O.No.'].astype(str).str.strip()
        df['GRR#'] = df['GRR#'].astype(str).str.strip()

        self.stdout.write(f"Found {len(df)} valid rows after cleaning.")

        # 4. Prepare Objects
        entries = []
        for _, row in df.iterrows():
            entries.append(GRRData(
                co_no=row['C.O.No.'],
                grr_no=row['GRR#'],
                po_no=str(row['P.O.No.']).strip(),
                grr_date=row['GRR.Date'] if pd.notna(row['GRR.Date']) else None,
                item_code=str(row['Item Cd']).strip(),
                description=str(row['Description']).strip(),
                supplier_name=str(row['Name']).strip(),
                rate=row['Rate'],
                received_qty=row['RcvdQty-SU']
            ))

        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"[DRY RUN] Would import {len(entries)} records."))
            return

        # 5. Atomic Bulk Import
        start_time = timezone.now()
        with transaction.atomic():
            deleted_count, _ = GRRData.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Cleared {deleted_count} old records."))

            batch_size = 5000
            for i in range(0, len(entries), batch_size):
                batch = entries[i:i + batch_size]
                GRRData.objects.bulk_create(batch)

        duration = (timezone.now() - start_time).total_seconds()
        self.stdout.write(self.style.SUCCESS(f"Imported {len(entries)} GRR records in {duration:.2f}s")) 