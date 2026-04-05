from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Module, ModulePermission, UserModulePermission
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds modules, permissions, and the complete user access matrix."

    def handle(self, *args, **kwargs):
        # 1. Seed Modules
        modules_data = [
            ('PROCUREMENT', 'Procurement'),
            ('PSR', 'PSR'),
            ('CAPACITY', 'Capacity'),
        ]
        module_objs = {code: Module.objects.get_or_create(code=code, defaults={'name': name})[0] 
                       for code, name in modules_data}

        # 2. Seed Permissions
        perms_data = [
            ('VIEW', 'View Only'),
            ('ADMIN', 'Admin'),
            ('PREPARER', 'Preparer'),
            ('APPROVER', 'Approver'),
        ]
        perm_objs = {code: ModulePermission.objects.get_or_create(code=code, defaults={'name': name})[0] 
                     for code, name in perms_data}

        # 3. Enhanced Helper Function
        def assign_access(username, first_name, last_name, mod_code, perm_code, role='employee', min_amt=None):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role,
                    'is_aprooved': True
                }
            )
            if created:
                user.set_password('InitialPass123!')
                user.save()

            try:
                # We use update_or_create to avoid ID/Unique constraint issues
                UserModulePermission.objects.update_or_create(
                    user=user,
                    module=module_objs[mod_code],
                    permission=perm_objs[perm_code],
                    defaults={'min_amount': min_amt, 'is_active': True}
                )
            except Exception as e:
                self.stderr.write(f"Failed for {username} on {mod_code}: {e}")
        # --- 4. DATA MAPPING (ROW BY ROW FROM SHEET) ---

        # MD - Raghuraj Deshpande
        assign_access('rdeshpande', 'Raghuraj', 'Deshpande', 'PROCUREMENT', 'ADMIN', min_amt=1000000)
        assign_access('rdeshpande', 'Raghuraj', 'Deshpande', 'PSR', 'ADMIN')
        assign_access('rdeshpande', 'Raghuraj', 'Deshpande', 'CAPACITY', 'APPROVER')

        # Head Assembly - Silvister Dwaraiswami
        assign_access('sdwaraiswami', 'Silvister', 'Dwaraiswami', 'PROCUREMENT', 'ADMIN')

        # Head - Project Team 1 - Abhijeet Gijare
        assign_access('agijare', 'Abhijeet', 'Gijare', 'PROCUREMENT', 'APPROVER')
        assign_access('agijare', 'Abhijeet', 'Gijare', 'PSR', 'PREPARER')
        assign_access('agijare', 'Abhijeet', 'Gijare', 'CAPACITY', 'PREPARER')

        # Head - Project Team 2 - Sumit Babel
        assign_access('sbabel', 'Sumit', 'Babel', 'PROCUREMENT', 'APPROVER')
        assign_access('sbabel', 'Sumit', 'Babel', 'PSR', 'PREPARER')
        assign_access('sbabel', 'Sumit', 'Babel', 'CAPACITY', 'PREPARER')

        # Head - Engineering - Sandeep Jawadwar
        assign_access('sjawadwar', 'Sandeep', 'Jawadwar', 'PROCUREMENT', 'APPROVER')
        assign_access('sjawadwar', 'Sandeep', 'Jawadwar', 'PSR', 'APPROVER')
        assign_access('sjawadwar', 'Sandeep', 'Jawadwar', 'CAPACITY', 'PREPARER')

        # Head - Purchase - Santosh Badam
        assign_access('sbadam', 'Santosh', 'Badam', 'PROCUREMENT', 'ADMIN')
        assign_access('sbadam', 'Santosh', 'Badam', 'CAPACITY', 'PREPARER')

        # Head - Finance & IT - Niranjan Panigrahi
        assign_access('npanigrahi', 'Niranjan', 'Panigrahi', 'PROCUREMENT', 'ADMIN', min_amt=200000)
        assign_access('npanigrahi', 'Niranjan', 'Panigrahi', 'PSR', 'ADMIN')
        assign_access('npanigrahi', 'Niranjan', 'Panigrahi', 'CAPACITY', 'ADMIN')

        # Design - Mechanical - Vipul Kamble
        assign_access('vkamble', 'Vipul', 'Kamble', 'PROCUREMENT', 'APPROVER')
        assign_access('vkamble', 'Vipul', 'Kamble', 'CAPACITY', 'PREPARER')

        # Purchase & Store Team (Procurement Preparers)
        store_team = [
            ('nmande', 'Narayan', 'Mande'), ('vwalhekar', 'Vikram', 'Walhekar'),
            ('rsawant', 'Rahul', 'Sawant'), ('schikaskar', 'Suyog', 'Chikaskar'),
            ('kraghuwanshi', 'Kiran', 'Raghuwanshi'), ('ngadhave', 'Nilesh', 'Gadhave'),
            ('okobal', 'Omkar', 'Kobal'), ('spawar', 'Shekhar', 'Pawar'),
            ('skulkarni', 'Sujeet', 'Kulkarni'), ('sanket_a', 'Sanket', 'Anantakawalas')
        ]
        for u, f, l in store_team:
            assign_access(u, f, l, 'PROCUREMENT', 'PREPARER')

        # Project Management Team (Procurement Approvers & PSR Preparers)
        pm_team = [
            ('rpunde', 'Rutvij', 'Punde'), ('akulkarni', 'Anirudha', 'Kulkarni'),
            ('rspravin', 'Raje Shripad', 'Pravin'), ('dsharma', 'Deepak', 'Sharma'),
            ('pshelke', 'Prabhat', 'Shelke')
        ]
        for u, f, l in pm_team:
            assign_access(u, f, l, 'PROCUREMENT', 'APPROVER')
            assign_access(u, f, l, 'PSR', 'PREPARER')

        # Finance and Accounts - Omkar Kulkarni
        assign_access('okulkarni_fin', 'Omkar', 'Kulkarni', 'PROCUREMENT', 'APPROVER')
        assign_access('okulkarni_fin', 'Omkar', 'Kulkarni', 'CAPACITY', 'APPROVER') # Corrected as per sheet

        # Technical Specialists (Capacity Preparers Only)
        tech_staff = [
            ('vbhadane', 'Vishal', 'Bhadane'), ('pkumar', 'Pawan', 'Kumar'),
            ('mkumar', 'Manoj', 'Kumar'), ('vvarpe', 'Vilas', 'Varpe'),
            ('vmatada', 'Vinay', 'Matada'), ('rzangruche', 'Rohit', 'Zangruche')
        ]
        for u, f, l in tech_staff:
            assign_access(u, f, l, 'CAPACITY', 'PREPARER')

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {User.objects.count()} users with exact matrix permissions."))