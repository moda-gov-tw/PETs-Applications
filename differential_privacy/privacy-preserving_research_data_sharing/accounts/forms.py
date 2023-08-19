from django.contrib.auth.forms import UserCreationForm

class TwUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = self.fields['username']
        password1 = self.fields['password1']
        password2 = self.fields['password2']
        
        self._set_display_class()
        self._set_label(username, password1, password2)
        self._set_suffix()
        self._set_help_text(username, password1, password2)
        self._set_error_message(username, password1, password2)
        
    def _set_display_class(self):
        for visible in self.visible_fields():
            pass
        
    def _set_label(self, username, password1, password2):
        username.label = '使用者名稱'
        password1.label = '密碼'
        password2.label = '密碼確認'
        
    def _set_suffix(self):
        for visible in self.visible_fields():
            visible.field.label_suffix = '：'
            
    def _set_help_text(self, username, password1, password2):
        username.help_text = '特殊符號僅接受@/./+/-/_'
        password1.help_text = '密碼至少8個字元，不能為全數字'
        password2.help_text = '請再次輸入密碼'
        
    def _set_error_message(self, username, password1, password2):
        username.error_messages['unique'] = '此名稱已被申請'
        username.error_messages['required'] = '請填寫使用者名稱'
        username.error_messages['max_length'] = '使用者名稱過長'
        username.error_messages['min_length'] = '使用者名稱過短'
        
        password1.error_messages['required'] = '請填寫密碼'
        password1.error_messages['max_length'] = '密碼過長'
        password1.error_messages['min_length'] = '密碼過短'
        
        password2.error_messages['required'] = '請填寫密碼確認'
        
        self.error_messages['password_mismatch'] = '密碼與密碼確認不一致'
        
class ChangePasswordForm(TwUserCreationForm):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False