from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'bookstore'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('inventory/', views.InventoryView.as_view(), name='inventory'),
    path('sales/', views.SalesView.as_view(), name='sales'),
    path('customer/', views.CustomerView.as_view(), name='customer'),
    path('supplier/', views.SupplierView.as_view(), name='supplier'),
]
