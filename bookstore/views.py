from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from .models import Customer


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


class CustomerView(LoginRequiredMixin, TemplateView):
    """
    Renders the customer management page, showing only the customers for the logged-in user.
    """
    template_name = "customers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch only the customers related to the logged-in user
        context['customers'] = Customer.objects.filter(user=self.request.user)
        return context

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ['phone', 'loyalty_points']
    template_name = 'customer_form.html'

    def form_valid(self, form):
        # Associate the new customer with the currently logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the customer management page after successful creation
        return reverse_lazy('bookstore:customer')

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['phone', 'loyalty_points']
    template_name = 'customer_form.html'

    def get_object(self, queryset=None):
        # Ensure that the customer being edited belongs to the current user
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'], user=self.request.user)
        return customer

    def get_success_url(self):
        # Redirect to the customer management page after successful update
        return reverse_lazy('bookstore:customer')

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'customer_confirm_delete.html'

    def get_object(self, queryset=None):
        # Ensure that the customer being deleted belongs to the current user
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'], user=self.request.user)
        return customer

    def get_success_url(self):
        # Redirect to the customer management page after successful deletion
        return reverse_lazy('bookstore:customer')

class SupplierView(TemplateView):
    """
    Renders the supplier and procurement management page.
    """
    template_name = "supplier.html"
