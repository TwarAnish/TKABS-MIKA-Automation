# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser
# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from django.utils.translation import gettext_lazy as _


# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'is_staff', 'is_active')
#     list_filter = ('role', 'is_staff', 'is_active')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
#         (_('Permissions'), {'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'phone_number'),
#         }),
#     )
#     search_fields = ('username', 'first_name', 'last_name', 'email')
#     ordering = ('username',)

# admin.site.register(CustomUser, CustomUserAdmin)


# # from django.shortcuts import render
# # from .decorators import role_required

# # @role_required('admin')
# # def admin_dashboard(request):
# #     return render(request, 'admin_dashboard.html')

# # @role_required('employee')
# # def employee_dashboard(request):
# #     return render(request, 'employee_dashboard.html')

# # {% if user.role == 'admin' %}
# #     <!-- Show admin-specific content -->
# # {% elif user.role == 'employee' %}
# #     <!-- Show employee-specific content -->
# # {% endif %}


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.translation import gettext_lazy as _


from django.contrib import admin
from .models import CustomUser, Module, ModulePermission, UserModulePermission

# Inline to see Module Access inside the User page
class UserModulePermissionInline(admin.TabularInline):
    model = UserModulePermission
    extra = 0
    fields = ('module', 'permission', 'min_amount', 'is_active')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'department', 'is_staff', 'is_active')
    list_filter = ('role', 'department', 'is_staff', 'is_active')          # ← added department filter
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Organization'), {'fields': ('role', 'department')}),           # ← grouped nicely
        (_('Permissions'), {'fields': ('is_aprooved', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),        
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'first_name', 'last_name', 'email',
                'password1', 'password2', 'role', 'department', 'phone_number'
            ),
        }),
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


@admin.register(UserModulePermission)
class UserModulePermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'permission', 'min_amount', 'is_active')
    list_filter = ('module', 'permission', 'user')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

# Only register these here (CustomUser is already registered via decorator above)
admin.site.register(Module)
admin.site.register(ModulePermission)
admin.site.register(CustomUser, CustomUserAdmin)