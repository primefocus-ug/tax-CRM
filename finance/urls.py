# finance/urls.py

from django.urls import path
from . import views 
app_name = 'finance'
urlpatterns = [
    
    
    path('dashboard/', views.finance_dashboard, name='dashboard'),
    path('expenses/', views.expenses_list_view, name='expenses_list'),
    path('expenses/form/', views.expense_create_view, name='expense_form'),
    path('expenses/form/<int:expense_id>/', views.expense_update_view, name='expense_update'),
    path('expenses/delete/<int:expense_id>/', views.expense_delete_view, name='expense_delete'),
    

    
]