from django import forms


class AddCatalogueForm(forms.Form):
    title = forms.CharField(label='Имя каталога', max_length=256, min_length=1)


class UploadFileForm(forms.Form):
    title = forms.CharField(label='Название', max_length=256)
    description = forms.CharField(label='Описание', widget=forms.Textarea)
    attributes = forms.CharField(label='Атрибуты', max_length=256)
    other_attributes = forms.CharField(label='Доп. аттрибуты', max_length=256, required=False)
    file = forms.FileField(label='Файл')
