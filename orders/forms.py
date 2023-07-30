from .models import Order
from django import forms

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'pin_code', 'address_line_1', 'address_line_2', 'country', 'city', 'state', 'order_note',]
    

class CouponApplyForm(forms.Form):
    code = forms.CharField(widget= forms.TextInput(attrs={'placeholder' : 'enter coupon code'}), label='')