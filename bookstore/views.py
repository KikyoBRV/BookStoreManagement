from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from .models import Customer, Book, Author, Publisher, Category
from .forms import BookForm

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

class HomeView(TemplateView):
    """
    Renders the home page with navigation to other sections.
    """
    template_name = 'bookstore/home.html'


class InventoryView(TemplateView):
    """
    Renders the inventory management page.
    """
    template_name = "bookstore/inventory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()  # Pass all books to the template
        return context

class BookCreateView(CreateView):
    """
    View to create a new book, handling both new and existing authors, publishers, and categories.
    """
    model = Book
    form_class = BookForm
    template_name = "bookstore/book_form.html"
    success_url = reverse_lazy('bookstore:inventory')

    def form_valid(self, form):
        # Handle Author
        if form.cleaned_data['new_author']:
            author, _ = Author.objects.get_or_create(name=form.cleaned_data['new_author'])
        else:
            author = form.cleaned_data['author']
        form.instance.author = author

        # Handle Publisher
        if form.cleaned_data['new_publisher']:
            publisher, _ = Publisher.objects.get_or_create(name=form.cleaned_data['new_publisher'])
        else:
            publisher = form.cleaned_data['publisher']
        form.instance.publisher = publisher

        # Handle Category
        if form.cleaned_data['new_category']:
            category, _ = Category.objects.get_or_create(name=form.cleaned_data['new_category'])
        else:
            category = form.cleaned_data['category']
        form.instance.category = category

        return super().form_valid(form)

class BookUpdateView(UpdateView):
    """
    View to update book details.
    """
    model = Book
    form_class = BookForm
    template_name = "bookstore/book_form.html"
    success_url = reverse_lazy('bookstore:inventory')

class BookDeleteView(DeleteView):
    """
    View to delete a book.
    """
    model = Book
    template_name = "bookstore/book_confirm_delete.html"
    success_url = reverse_lazy('bookstore:inventory')


class SalesView(TemplateView):
    """
    Renders the sales processing page.
    """
    template_name = "bookstore/sales.html"


class CustomerView(LoginRequiredMixin, TemplateView):
    """
    Renders the customer management page, showing only the customers for the logged-in user.
    """
    template_name = "bookstore/customers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch only the customers related to the logged-in user
        context['customers'] = Customer.objects.filter(user=self.request.user)
        return context

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ['phone', 'loyalty_points']
    template_name = 'bookstore/customer_form.html'

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
    template_name = 'bookstore/customer_form.html'

    def get_object(self, queryset=None):
        # Ensure that the customer being edited belongs to the current user
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'], user=self.request.user)
        return customer

    def get_success_url(self):
        # Redirect to the customer management page after successful update
        return reverse_lazy('bookstore:customer')

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'bookstore/customer_confirm_delete.html'

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
