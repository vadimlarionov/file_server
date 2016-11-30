from django import forms


class AddCatalogueForm(forms.Form):
    title = forms.CharField(max_length=256, min_length=1, label='Имя каталога')


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField(label='Файл')
