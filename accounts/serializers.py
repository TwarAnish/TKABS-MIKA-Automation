# serializers.py
from rest_framework import serializers
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from capacity_planning.models import Department

from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])


class SuperuserResetPasswordSerializer(serializers.Serializer):
#    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])


# from capacity_planning.models import Department
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email',
            'role', 'phone_number',
            'is_staff', 'is_active'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'phone_number': {'required': True},
        }

    def create(self, validated_data):
        # Extract password and username before passing the rest as **validated_data
        password = validated_data.pop('password', None)
        username = validated_data.pop('username')  # Remove from validated_data after extracting
        
        user = CustomUser.objects.create_user(
            username=username,  # Pass as positional/keyword argument
            password=password,  # Pass as keyword argument
            **validated_data    # Pass remaining fields (without username)
        )
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            # Public / unauthenticated → hide everything sensitive
            sensitive_fields = ['phone_number', 'email']
            for field in sensitive_fields:
                ret[field] = None
            return ret

        user = request.user

        # Employees can only see their own full data
        if user.role == 'employee' and instance != user:
            sensitive_fields = ['phone_number', 'email']
            for field in sensitive_fields:
                ret[field] = None if instance != user else ret[field]

        # Admins can see employee data but not other admins/superusers full sensitive info
        elif user.role == 'admin':
            if instance.role in ['admin', 'superuser']:
                ret['phone_number'] = '***HIDDEN***'

        # Superuser sees everything (or you can still mask if you want)
        elif user.role == 'superuser':
            pass  # show all

        return ret

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            if not user.is_aprooved: # Checking your custom field
                raise serializers.ValidationError("User account is not approved yet.")
            return user
        raise serializers.ValidationError("Invalid credentials.")        
    
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone_number', 'role', 'department', 'password'
        ]

    def validate_role(self, value):
        if value == 'superuser':
            raise serializers.ValidationError("Cannot create superuser via API")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.is_aprooved = True   # usually starts as not approved
        user.save()
        return user

class UserModulePermissionDetailSerializer(serializers.ModelSerializer):
    # Optional: Bring in the names of the module and permission for readability
    module_name = serializers.CharField(source='module.name', read_only=True)
    permission_name = serializers.CharField(source='permission.name', read_only=True)

    class Meta:
        model = UserModulePermission
        fields = [
            'id', 'module', 'module_name', 
            'permission', 'permission_name', 
            'min_amount', 'is_active'
        ]

class UserListSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    permissions = UserModulePermissionDetailSerializer(
        source='usermodulepermission_set', 
        many=True, 
        read_only=True
    )
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'phone_number', 'role',
            'department', 'department_name',
            'is_active', 'is_aprooved','permissions'
        ]