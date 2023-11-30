from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.add_inventory_item, name='add_inventory_item'),
    path('edit/<int:pk>/', views.edit_inventory_item, name='edit_inventory_item'),
    path('delete/<int:pk>/', views.delete_inventory_item, name='delete_inventory_item'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

