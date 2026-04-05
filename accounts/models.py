from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class Department(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.PositiveIntegerField(default=0, help_text="For UI sorting")
    icon_text = models.CharField(max_length=50, blank=True, help_text="Short text/icon for UI (e.g. 'DE', 'PE')")
    
    # Optional: Add level field for easier querying
    level = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Department"
        unique_together = ['parent', 'name']  # Prevent duplicate names under same parent

    def save(self, *args, **kwargs):
        # Calculate the level based on parent hierarchy
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)
        
        # Update children levels if this is a new record or parent changed
        if hasattr(self, '_update_children'):
            self.update_children_levels()

    def update_children_levels(self):
        """Recursively update levels of all children"""
        for child in self.children.all():
            child.level = self.level + 1
            child.save()
            child.update_children_levels()

    def get_full_path(self):
        """Return the full path from root to this department"""
        if self.parent:
            return f"{self.parent.get_full_path()} → {self.name}"
        return self.name

    def get_ancestors(self):
        """Return all ancestor departments"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return reversed(ancestors)

    def get_descendants(self):
        """Return all descendant departments"""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    def __str__(self):
        # You can customize this based on how you want to display the hierarchy
        return self.get_full_path()
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username must be set'))
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'superuser')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') != 'superuser':
            raise ValueError(_('Superuser must have role "superuser"'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('superuser', 'Superuser'),
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('md','Managing Director'),
        ('hod','Head of Department'),
        ('project_manager','Project Manager'),
        ('deputy_manager','Deputy Manager'),
        ('assistant_manager','Assistant Manager')
    )

    first_name = models.CharField(_('First Name'), max_length=30)
    last_name = models.CharField(_('Last Name'), max_length=30)
    email = models.EmailField(_('Email Address'), unique=True, blank=True, null=True)
    username = models.CharField(_('Username'), max_length=150, unique=True)
    password = models.CharField(_('Password'), max_length=128)
    role = models.CharField(_('Role'), max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(_('Phone Number'),null=True,blank=True, max_length=15, unique=True, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_('Phone number must be entered in the format +919876543210 or 9876543210'))])

    is_staff = models.BooleanField(_('Staff Status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    is_aprooved = models.BooleanField(default=False)
    objects = CustomUserManager()
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        related_name='accounts_department',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    class Meta:
        permissions = [
            ('can_view_employee_data', 'Can view employee data'),
            ('can_view_admin_data', 'Can view admin data'),
            ('can_view_superuser_data', 'Can view superuser data'),
        ]

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()




class Module(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ModulePermission(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class UserModulePermission(models.Model):
    id = models.BigAutoField(primary_key=True) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    permission = models.ForeignKey(ModulePermission, on_delete=models.CASCADE)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'module', 'permission')



