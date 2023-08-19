from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# https://stackoverflow.com/questions/18392405/issue-trying-to-change-language-from-django-template
@register.filter
def remove_language_code(url):
    return '/'+url.split('/', 2)[-1]