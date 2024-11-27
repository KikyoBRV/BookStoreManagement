from django import forms
from .models import Book, Author, Publisher, Category, Order, OrderItem, \
    Purchase


class BookForm(forms.ModelForm):
    """
    Form for adding a new book with options to choose existing or add new Author, Publisher, and Category.
    """
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
        label='Select Existing Author'
    )
    new_author = forms.CharField(
        max_length=255,
        required=False,
        label='Or Add New Author'
    )
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        label='Select Existing Publisher'
    )
    new_publisher = forms.CharField(
        max_length=255,
        required=False,
        label='Or Add New Publisher'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Select Existing Category'
    )
    new_category = forms.CharField(
        max_length=255,
        required=False,
        label='Or Add New Category'
    )

    class Meta:
        model = Book
        fields = [
            'title', 'description', 'price', 'quantity_in_stock',
            'publication_year', 'publication_month'
        ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'payment_method', 'total_amount']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['book', 'amount']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['total_cost']