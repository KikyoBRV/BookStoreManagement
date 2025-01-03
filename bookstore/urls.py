from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'bookstore'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('search-books/', views.search_books, name='search_books'),
    path('inventory/', views.InventoryView.as_view(), name='inventory'),
    path('inventory/create/', views.BookCreateView.as_view(), name='book_create'),
    path('inventory/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('inventory/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('sales/', views.SalesView.as_view(), name='sales'),
    path('sales/add/', views.AddOrderView.as_view(), name='add_order'),
    path('customer/', views.CustomerView.as_view(), name='customer'),
    path('customer/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customer/lookup/', views.lookup_customer, name='customer_lookup'),
    path('sales/create/', views.create_order, name='create_order'),
    path('sales/static/', views.sales_statistic_page, name='sales_static_page'),
    path('customer/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_edit'),
    path('customer/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    path('supplier/', views.SupplierView.as_view(), name='supplier'),
    path('supplier/add/', views.AddPurchaseView.as_view(),
         name='add_purchase'),
    path('supplier/create/', views.create_purchase, name='create_purchase'),
    path('supplier/static/', views.supplier_statistic_page, name='supplier_static_page'),

]
