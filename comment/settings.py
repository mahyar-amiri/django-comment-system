from django.conf import settings
from django.urls import reverse_lazy

_COMMENT_SETTINGS = getattr(settings, 'COMMENT_SETTINGS', {})
login_url = getattr(settings, 'LOGIN_URL')

COMMENT_SETTINGS = {
    'LOGIN_URL': reverse_lazy(login_url) if type(login_url) == str else login_url,
    'LANGUAGE_CODE': getattr(settings, 'LANGUAGE_CODE'),
    'URLHASH_LENGTH': _COMMENT_SETTINGS.get('URLHASH_LENGTH', 8),
    'OFFLINE_IMPORTS': _COMMENT_SETTINGS.get('OFFLINE_IMPORTS', True),
    'PROFILE_IMAGE_FIELD': _COMMENT_SETTINGS.get('PROFILE_IMAGE_FIELD', None),
}
