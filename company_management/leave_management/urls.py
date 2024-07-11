from django.urls import path
from . import views

urlpatterns = [
    path('leave/apply/', views.LeaveApplyAPIView.as_view(), name='leave'),
    path('leave/approve/<int:id>/', views.LeaveApproveAPIView.as_view(), name='leave'),

    path('leave-type/', views.LeaveTypeCRUDAPIView.as_view(), name='leavetype_crud'),
    path('leave-type/<int:id>/', views.LeaveTypeCRUDAPIView.as_view(), name='leavetype_crud'),

    path('leave-rule/', views.LeaveRuleCRUDAPIView.as_view(), name='role_crud'),
    path('leave-rule/<int:id>/', views.LeaveRuleCRUDAPIView.as_view(), name='role_crud'),
]
