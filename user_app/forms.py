from django import forms


class AddCatalogueForm(forms.Form):
    title = forms.CharField(label='Имя каталога', max_length=256, min_length=1)


class FileForm(forms.Form):
    CHOICES = (
        ('1', 'audio',),
        ('2', 'video',),
        ('3', 'text',),
        ('4', 'image',),
        ('5', 'read only',),
        ('6', 'executable',),
        ('7', 'zipped',)
    )

    title = forms.CharField(label='Название', max_length=256)
    description = forms.CharField(label='Описание', widget=forms.Textarea, required=False)
    attributes = forms.MultipleChoiceField(label='Атрибуты', widget=forms.CheckboxSelectMultiple,
                                           choices=CHOICES, required=False)
    other_attributes = forms.CharField(label='Доп. аттрибуты', max_length=256, required=False)

    def clean_attributes(self):
        return ' '.join(
            [value for key, value in self.CHOICES if key in self.cleaned_data['attributes']]
        )


class UploadFileForm(FileForm):
    file = forms.FileField(label='Файл')


class EditFileForm(FileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['attributes'] = [key for key, value in self.CHOICES
                                      if value in self.initial.get('attributes', [])]


class FileDeleteForm(forms.Form):
    file_id = forms.IntegerField(widget=forms.HiddenInput)


class CatalogueDeleteForm(forms.Form):
    catalogue_id = forms.IntegerField(widget=forms.HiddenInput)
