from django import forms
from django_countries.fields import CountryField
import uuid 
class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="First name", widget=forms.TextInput(
                              attrs={'class': "form-control"}) ) 
    last_name = forms.CharField(max_length=50, label="Last name", widget=forms.TextInput(
                              attrs={'class': "form-control"}) )
    email = forms.CharField(max_length=50, label="payment email", widget=forms.TextInput(
                              attrs={'class': "form-control"}) )
    address = forms.CharField(max_length=250, label="Adress", widget=forms.TextInput(
                              attrs={'class': "form-control"}) )
    city = forms.CharField(max_length=100, label="Town", widget=forms.TextInput(
                              attrs={'class': "form-control"}) )
    post_code = forms.CharField(max_length=20, label="Postcode", widget=forms.TextInput(
                              attrs={'class': "form-control"}) )
    
    order_key = forms.CharField(widget=forms.HiddenInput(), required=True) 
    
        
    Options = [
            ('1', 'Choose...'),
            ('2', 'Surrey'),
            ('3', 'Birkshire'),
        ]
    county = forms.ChoiceField(label='County', widget=forms.Select(
                              attrs={'class': "form-control"}), choices=Options)

    
    Options = [
                ('1', 'Choose...'),
                ('2', 'England'),
                ('3', 'Scotland'),
                ('4', 'Ireland'),
            ]
            
    country = forms.ChoiceField(label='Country', widget=forms.Select(
                            attrs={'class': "form-control"}), choices=Options)

    