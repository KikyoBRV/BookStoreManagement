from django.views.generic import TemplateView

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
