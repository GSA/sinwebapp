from django import forms

class UploadFileForm(forms.Form):
    sin_number = forms.CharField(max_length=100)
    file = forms.FileField()