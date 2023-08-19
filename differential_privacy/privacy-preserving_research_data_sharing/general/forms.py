from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class AbstractForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_display_class()
        self._set_suffix()
        self._set_error_message()
        
    def _set_display_class(self):
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'big-input-arrow'
                
    def _set_suffix(self):
        for visible in self.visible_fields():
            visible.field.label_suffix = '：'
            
    def _set_error_message(self):
        for visible in self.visible_fields():
            visible.field.error_messages['required'] = '此為必填欄位'