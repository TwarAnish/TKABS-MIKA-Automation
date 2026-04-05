# views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import IsSuperuser, IsAdminOrSuperuser, IsOwnerOrAdmin
from .pagination import CustomUserCursorPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate
from .models import UserModulePermission
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from .models import CustomUser

# 1. Self Password Change (Requires Old Password)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # set_password hashes the password automatically
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. Superuser Reset (Forgot Password - No Old Password Required)
class SuperuserResetUserPasswordView(APIView):
    permission_classes = [IsAuthenticated] # We will check for superuser inside

    def post(self, request, user_id):
        # Security Check: Only allow Superuser or Admin role from your choices
        if not request.user.is_superuser and request.user.role != 'superuser':
            return Response({"error": "Only Superusers can reset other users' passwords."}, 
                            status=status.HTTP_403_FORBIDDEN)

        target_user = get_object_or_404(CustomUser, id=user_id)
        serializer = SuperuserResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            target_user.set_password(serializer.data.get("new_password"))
            target_user.save()
            return Response({"message": f"Password for {target_user.username} has been reset."}, 
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# 1. Registration (anyone can register as employee by default)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Force normal users to be 'employee' unless superuser is creating
        if not self.request.user.is_authenticated or self.request.user.role != 'superuser':
            serializer.validated_data['role'] = 'employee'
        serializer.save()

# 2. List all users - only admin & superuser
class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminOrSuperuser]
    pagination_class = CustomUserCursorPagination

# 3. Retrieve, Update, Delete single user
class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsOwnerOrAdmin]  # Owner or admin/superuser

    # Allow users to update their own profile (partial)
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

# Optional: Current user profile endpoint (very useful for Angular)
class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginSerializer,  # This tells Swagger what the input form looks like
        responses={200: LoginSerializer}, # This tells Swagger what the output looks like
    )

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_aprooved: # Your custom model field
                return Response({"detail": "Account pending approval."}, status=status.HTTP_403_FORBIDDEN)
            user_role=user.role.lower()
            if user.department and user.role:
                if user.department.name.lower() == 'purchase' and user.role.lower() == 'employee':
                    user_role = 'buyer'
            
            
            refresh = RefreshToken.for_user(user)

            perms = UserModulePermission.objects.filter(
                user=user,
                is_active=True
            ).values('module__code', 'permission__code').distinct()

            module_summary = {}
            for p in perms:
                mod = p['module__code']
                role = p['permission__code']
                if mod not in module_summary:
                    module_summary[mod] = []
                if role not in module_summary[mod]:
                    module_summary[mod].append(role)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'username': user.username,
                    'role': user_role,
                    'first_name': user.first_name,
                    'department': user.department.name if user.department else None
                },
                'permissions': module_summary
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        


class UsersAPIView(APIView):
    """
    POST    /api/users/     → create user (registration)
    GET     /api/users/     → list users (staff only)
    """
    permission_classes = [permissions.AllowAny]   # ← open registration
    # If you want to restrict both → change to permissions.IsAuthenticated or IsAdminUser

    def get(self, request):
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to view users."},
                status=status.HTTP_403_FORBIDDEN
            )

        queryset = CustomUser.objects.select_related('department').order_by('first_name', 'last_name')

        # Optional filters
        role = request.query_params.get('role')
        dept = request.query_params.get('department')
        search = request.query_params.get('search')

        if role:
            queryset = queryset.filter(role=role)
        if dept:
            queryset = queryset.filter(department_id=dept)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )

        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        return Response(
            UserListSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    def patch(self, request):
        user_id = request.data.get('id')
        new_role = request.data.get('role')

        # 1. Validate input
        if not user_id:
            return Response({"detail": "User 'id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not new_role:
            return Response({"detail": "New 'role' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Permission Check (Only staff/admins should change roles)
        if not request.user.is_staff:
            return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

        # 3. Find user and update
        user = get_object_or_404(CustomUser, pk=user_id)
        
        # Check if role is valid based on your ROLE_CHOICES
        valid_roles = [choice[0] for choice in CustomUser.ROLE_CHOICES]
        if new_role not in valid_roles:
            return Response(
                {"detail": f"Invalid role. Choose from: {', '.join(valid_roles)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user.role = new_role
        user.save()

        # 4. Return updated user data
        return Response({
            "message": "Role updated successfully",
            "user": UserListSerializer(user).data
        }, status=status.HTTP_200_OK)



class UserMetadataAPIView(APIView):
    """
    GET /api/users/metadata/
    Returns choices for dropdowns: roles + departments
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        roles = [
            {"value": value, "label": label}
            for value, label in CustomUser.ROLE_CHOICES
        ]

        departments = Department.objects.values("id", "name").order_by("name")
        # If your Department model uses different field → change "name" accordingly

        return Response({
            "roles": roles,
            "departments": list(departments)
        })
    

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
class GrantUserPermissionView(APIView):
    """
    POST: Bulk assign permissions (module/permission lists).
    PATCH: Update a specific UserModulePermission record via 'id'.
    """

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        # 1. Extract data
        module_names = request.data.get('module', [])
        permission_names = request.data.get('permission', [])
        min_amount = request.data.get('min_amount')

        # Ensure we have lists to iterate over
        if not isinstance(module_names, list) or not isinstance(permission_names, list):
            return Response(
                {"error": "Fields 'module' and 'permission' must be lists."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        results = []
        errors = []

        # 2. Loop through combinations
        for m_name in module_names:
            for p_name in permission_names:
                try:
                    module_obj = Module.objects.get(name__iexact=m_name)
                    perm_obj = ModulePermission.objects.get(name__iexact=p_name)

                    # Create or Update the specific row
                    user_perm, created = UserModulePermission.objects.update_or_create(
                        user=user,
                        module=module_obj,
                        permission=perm_obj,
                        defaults={
                            'min_amount': min_amount if min_amount else None,
                            'is_active': True
                        }
                    )
                    results.append({
                        "id": user_perm.id,
                        "module": module_obj.name,
                        "permission": perm_obj.name,
                        "status": "created" if created else "updated"
                    })
                except Module.DoesNotExist:
                    errors.append(f"Module '{m_name}' not found.")
                except ModulePermission.DoesNotExist:
                    errors.append(f"Permission '{p_name}' not found.")

        return Response({
            "status": "success",
            "assignments": results,
            "errors": errors
        }, status=status.HTTP_201_CREATED)

    def patch(self, request, user_id=None):
        # 1. Determine which user we are talking about
        # Priority: URL parameter, then Body payload
        effective_user_id = user_id or request.data.get('user_id')
        record_id = request.data.get('id')

        if not record_id:
            return Response({"error": "Record 'id' is required."}, status=400)

        # 2. Fetch the specific permission record
        # We filter by user_id to ensure the user actually owns this permission record
        if effective_user_id:
            user_perm = get_object_or_404(UserModulePermission, id=record_id, user_id=effective_user_id)
        else:
            user_perm = get_object_or_404(UserModulePermission, id=record_id)

        # 3. Handle string-based lookups for Module and Permission
        # We MUST remove these from the data before the serializer sees them
        mutable_data = request.data.copy()
        new_module_name = mutable_data.pop('module', None)
        new_perm_name = mutable_data.pop('permission', None)

        try:
            if new_module_name:
                user_perm.module = Module.objects.get(name__iexact=new_module_name)
            
            if new_perm_name:
                user_perm.permission = ModulePermission.objects.get(name__iexact=new_perm_name)
            
            # Save manually updated foreign keys
            if new_module_name or new_perm_name:
                user_perm.save()

        except Module.DoesNotExist:
            return Response({"error": f"Module '{new_module_name}' not found."}, status=404)
        except ModulePermission.DoesNotExist:
            return Response({"error": f"Permission '{new_perm_name}' not found."}, status=404)

        # 4. Use the serializer for remaining fields (min_amount, is_active)
        # We pass 'mutable_data' which NO LONGER contains the 'module' or 'permission' strings
        serializer = UserModulePermissionDetailSerializer(user_perm, data=mutable_data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)