from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete/<log_id>/', views.delete_log, name='delete_log'),
    path('edit/<log_id>/', views.edit_log, name='edit_log'),
    path('complete/<log_id>/', views.complete_pending, name='complete_pending'),
]