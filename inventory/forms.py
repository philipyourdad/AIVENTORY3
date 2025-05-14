from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        self.fields['price'].widget.attrs.update({'class': 'textinput form-control', 'min': '0', 'step': '0.01'})
        self.fields['price'].label = "Price Per Piece"

    class Meta:
        model = Stock
        fields = ['name', 'quantity', 'price']
