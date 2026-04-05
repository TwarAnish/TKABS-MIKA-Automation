from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # Superuser resets someone else's by ID
    path('reset-user-password/<int:user_id>/', SuperuserResetUserPasswordView.as_view(), name='superuser-reset'),  
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', CustomUserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path('users_account/', UsersAPIView.as_view(), name='user_create'),    
    path('users/metadata/', UserMetadataAPIView.as_view(), name='user_meta'),    
    path('user_permission/<int:user_id>/', GrantUserPermissionView.as_view(), name='grant-permission'),
    
]