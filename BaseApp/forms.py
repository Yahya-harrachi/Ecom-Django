from django import forms
from .models import Product
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    # user_id = forms.ModelChoiceField(
    #     queryset=User.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
    #     label="User"
    # )
    class Meta:
        model = Product
        fields = '__all__'