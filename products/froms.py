from django import forms
class ProductFrom(forms.Form):
    title = forms.CharField(max_length=50)
    image = forms.FileField()
