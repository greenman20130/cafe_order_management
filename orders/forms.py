from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    item_name = forms.CharField(max_length=100, required=False)
    item_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Order
        fields = ['table_number', 'item_name', 'item_price']