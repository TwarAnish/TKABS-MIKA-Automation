"""
Create a superuser for the Django application
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SRC.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role='ADMIN'
    )
    print("✓ Superuser created successfully!")
    print("  Username: admin")
    print("  Password: admin123")
else:
    print("✓ Superuser already exists")
