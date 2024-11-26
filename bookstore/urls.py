from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'bookstore'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('inventory/', views.InventoryView.as_view(), name='inventory'),
    path('inventory/create/', views.BookCreateView.as_view(), name='book_create'),
    path('inventory/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('inventory/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('sales/', views.SalesView.as_view(), name='sales'),
    path('customer/', views.CustomerView.as_view(), name='customer'),
    path('customer/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customer/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_edit'),
    path('customer/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    path('supplier/', views.SupplierView.as_view(), name='supplier'),
]
