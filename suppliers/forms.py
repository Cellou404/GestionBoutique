from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from suppliers.models import Suppliers


class SupplierCreateUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Suppliers
        fields = ("name", "email", "phone", "address", "town")
