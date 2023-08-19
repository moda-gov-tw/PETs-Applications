#document https://docs.djangoproject.com/en/2.0/_modules/django/contrib/auth/password_validation/#MinimumLengthValidator
import gzip
import os
import re
from difflib import SequenceMatcher

from django.contrib.auth.password_validation import MinimumLengthValidator
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.contrib.auth.password_validation import NumericPasswordValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext, gettext

class TwMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "密碼長度過短，長度至少為 %(min_length)d ",
                    "密碼長度過短，長度至少為 %(min_length)d ",
                    self.min_length
                ),
            code='password_too_short',
            params={'min_length': self.min_length},
        )
        
    def get_help_text(self):
       return ngettext(
           "密碼長度至少為 %(min_length)d ",
           "密碼長度至少為 %(min_length)d ",
           self.min_length
       ) % {'min_length': self.min_length}
       
class TwUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        gettext("密碼與 %(verbose_name)s 欄位過於相似"),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return gettext("密碼不能與其他欄位過於相似.")
        
class TwCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                gettext("密碼太過常見"),
                code='password_too_common',
            )

    def get_help_text(self):
        return gettext("不能使用常見密碼")
        
class TwNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                gettext("密碼全為數字"),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return gettext("密碼不能全為數字")
