from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

class HomeView(TemplateView):
    """
    Renders the home page with navigation to other sections.
    """
    template_name = "home.html"


class InventoryView(TemplateView):
    """
    Renders the inventory management page.
    """
    template_name = "inventory.html"


class SalesView(TemplateView):
    """
    Renders the sales processing page.
    """
    template_name = "sales.html"


class CustomerView(TemplateView):
    """
    Renders the customer management page.
    """
    template_name = "customers.html"


class SupplierView(TemplateView):
    """
    Renders the supplier and procurement management page.
    """
    template_name = "supplier.html"
