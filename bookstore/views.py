from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from .models import Customer, Book, Author, Publisher, Category, Order, \
    OrderItem
from .forms import BookForm, OrderForm


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

class HomeView(TemplateView):
    """
    Renders the home page with navigation to other sections.
    """
    template_name = 'bookstore/home.html'


class InventoryView(LoginRequiredMixin, TemplateView):
    """
    Renders the inventory management page.
    """
    template_name = "bookstore/inventory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter books by the logged-in user
        context['books'] = Book.objects.filter(user=self.request.user)
        return context


@login_required
def search_books(request):
    query = request.GET.get('q', '').strip()

    if query:
        books = Book.objects.filter(
            title__icontains=query,
            user=request.user  # Filter by the logged-in user
        ).values('id', 'title', 'author__name', 'publisher__name', 'category__name', 'price', 'quantity_in_stock')[:10]
    else:
        # If no query, return all books
        books = Book.objects.filter(user=request.user).values('id', 'title', 'author__name', 'publisher__name', 'category__name', 'price', 'quantity_in_stock')[:10]

    return JsonResponse(list(books), safe=False)

class BookCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new book, handling both new and existing authors, publishers, and categories.
    """
    model = Book
    form_class = BookForm
    template_name = "bookstore/book_form.html"
    success_url = reverse_lazy('bookstore:inventory')

    def form_valid(self, form):
        # Set the logged-in user as the owner of the book
        form.instance.user = self.request.user

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

class BookUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update book details.
    """
    model = Book
    form_class = BookForm
    template_name = "bookstore/book_form.html"
    success_url = reverse_lazy('bookstore:inventory')

    def get_queryset(self):
        # Ensure users can only update their own books
        return Book.objects.filter(user=self.request.user)

class BookDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete a book.
    """
    model = Book
    template_name = "bookstore/book_confirm_delete.html"
    success_url = reverse_lazy('bookstore:inventory')

    def get_queryset(self):
        # Ensure users can only delete their own books
        return Book.objects.filter(user=self.request.user)

class SalesView(ListView):
    """
    Displays a list of orders and supports filtering by date.
    """
    model = Order
    template_name = "bookstore/sales.html"
    context_object_name = 'orders'

    def get_queryset(self):
        # Get all orders
        queryset = super().get_queryset()

        # Check if a date filter is provided
        date_filter = self.request.GET.get('date')
        if date_filter:
            date_obj = parse_date(date_filter)
            if date_obj:
                queryset = queryset.filter(order_date=date_obj)

        return queryset

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Handle AJAX requests
            date_filter = request.GET.get('date')
            queryset = self.get_queryset()
            data = {
                'orders': [
                    {
                        'id': order.id,
                        'customer_name': order.customer.name,
                        'order_date': order.order_date.strftime('%Y-%m-%d'),
                        'payment_method': order.payment_method,
                        'total_amount': order.total_amount,
                        'order_items': [
                            {
                                'book_title': item.book.title,
                                'amount': item.amount
                            }
                            for item in order.orderitem_set.all()
                        ]
                    }
                    for order in queryset
                ]
            }
            return JsonResponse(data)
        return super().get(request, *args, **kwargs)

class AddOrderView(CreateView):
    """
    Handles the creation of a new order and sends a list of available books
    to the order_form template.
    """
    model = Order
    form_class = OrderForm
    template_name = "bookstore/order_form.html"
    success_url = reverse_lazy('bookstore:sales')

    def get_context_data(self, **kwargs):
        """
        Add the list of books to the context, making them available to the template.
        """
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()  # Fetch all books
        return context

    def form_valid(self, form):
        """
        Override form_valid to create OrderItems for each selected book
        and recalculate the total amount for the Order.
        """
        # First, save the Order (this creates the Order object)
        response = super().form_valid(form)

        # Get the created Order object
        order = self.object

        # Loop through each order item and create OrderItem instances
        order_items_data = self.request.POST  # Get the data from the form submission
        order_item_count = len(
            [key for key in order_items_data if key.startswith('book-')])

        for i in range(1, order_item_count + 1):
            book_id = order_items_data.get(f'book-{i}')
            amount = order_items_data.get(f'amount-{i}')

            if book_id and amount:
                # Fetch the Book object
                book = Book.objects.get(id=book_id)

                # Create the OrderItem
                OrderItem.objects.create(
                    order=order,  # Associate with the Order
                    book=book,  # Set the Book
                    amount=amount  # Set the amount
                )

        # Recalculate the total amount for the Order
        total_amount = sum(item.amount * item.book.price for item in
                           order.orderitem_set.all())
        order.total_amount = total_amount
        order.save()

        return response


def lookup_customer(request):
    phone = request.GET.get('phone')
    if phone:
        try:
            customer = Customer.objects.get(phone=phone)
            return JsonResponse({'customer': {'name': customer.name}})
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
    return JsonResponse({'error': 'No phone number provided'}, status=400)

def create_order(request):
    if request.method == 'POST':
        customer_phone = request.POST.get('customer-phone')
        payment_method = request.POST.get('payment-method')

        # Get customer object
        customer = Customer.objects.filter(phone=customer_phone).first()
        if not customer:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        # Initialize total amount for the order
        total_amount = 0
        order_items = []

        # Create the Order first to get an order_id
        order = Order.objects.create(
            customer=customer,
            payment_method=payment_method,
            total_amount=0  # We'll update total_amount later
        )

        # Iterate through the items submitted in the form
        for i in range(1, len(request.POST) // 2):  # Assuming two fields per order item (book, amount)
            book_id = request.POST.get(f'book-{i}')
            amount = request.POST.get(f'amount-{i}')

            if book_id and amount:
                try:
                    book = Book.objects.get(id=book_id)
                except Book.DoesNotExist:
                    continue  # Ignore invalid book IDs

                amount = int(amount)

                # Create OrderItem and associate with the order
                order_item = OrderItem(book=book, amount=amount, order=order)
                order_item.save()

                # Add the item price to total amount
                total_amount += book.price * amount

                # Update Book's quantity in stock
                book.quantity_in_stock -= amount
                book.save()

                order_items.append(order_item)

        # Update the total amount for the Order after all OrderItems are created
        order.total_amount = total_amount
        order.save()

        # Redirect to the sales page after order is created
        return redirect('bookstore:sales')

    return JsonResponse({'error': 'Invalid request method'}, status=400)

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
    fields = ['name', 'phone', 'loyalty_points']
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
    fields = ['name', 'phone', 'loyalty_points']
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
    template_name = "bookstore/supplier.html"
