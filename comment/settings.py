from django.conf import settings

_COMMENT_SETTINGS = getattr(settings, "COMMENT_SETTINGS", {})

COMMENT_SETTINGS = {
    'LOGIN_URL': getattr(settings, 'LOGIN_URL'),
    'LANGUAGE_CODE': getattr(settings, 'LANGUAGE_CODE'),
    'URLHASH_LENGTH': _COMMENT_SETTINGS.get('URLHASH_LENGTH', 8),
    'OFFLINE_IMPORTS': _COMMENT_SETTINGS.get('OFFLINE_IMPORTS', True),
    'PROFILE_IMAGE_FIELD': _COMMENT_SETTINGS.get('PROFILE_IMAGE_FIELD', None),
}
