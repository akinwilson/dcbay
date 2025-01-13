from django import forms 

class ReviewForm(forms.Form):

    comment = forms.CharField(label="comment", initial="", max_length=320, required=False)
    rate= forms.IntegerField(label="rate", min_value=1, max_value=5, initial=5, )
    orderId = forms.IntegerField(label="orderId")
