from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserCRUDAPIView.as_view(), name="usercrud"),
    path('user/login/', views.UserLoginView.as_view(), name="login"),
    path('user/register/', views.UserRegistrationView.as_view(), name="login"),
    path('user/<int:id>/', views.UserCRUDAPIView.as_view(), name="usercruddetail"),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('user/<int:pk>/update-role/', views.UserUpdateRoleAPIView.as_view(), name='user-update-role'),
]
