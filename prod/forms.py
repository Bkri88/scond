from django import forms
from .models import Category, Product, Staff, Sale

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity_available']

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['user','first_name','email','phone_num','national_id' ,'position','salary', 'profile_picture']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product','staff','quantity_sold','sold_amount','is_loan']

# forms.py