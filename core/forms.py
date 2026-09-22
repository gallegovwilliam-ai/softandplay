from django.forms import ModelForm

class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
        	field.widget.attrs['class'] = 'form-control'