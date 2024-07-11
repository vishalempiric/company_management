from django.urls import path
from . import views

urlpatterns = [
    path('role/', views.RoleCRUDAPIView.as_view(), name='role_crud'),
    path('role/<int:id>/', views.RoleCRUDAPIView.as_view(), name='role_crud'),
]
