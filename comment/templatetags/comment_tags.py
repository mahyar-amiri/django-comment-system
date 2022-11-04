from django import template
from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static

from comment import settings

register = template.Library()


@register.inclusion_tag('comment/comments.html')
def render_comments(request, obj):
    context = {
        'object': obj,
        'request': request,
        'object_info': {
            'app_name': type(obj)._meta.app_label,
            'model_name': type(obj).__name__,
            'content_type': ContentType.objects.get_for_model(obj),
            'object_id': obj.id
        }
    }
    return context


@register.simple_tag
def comment_count_children(parent_comment):
    return parent_comment.children.filter_accepted().count()


@register.simple_tag
def comment_login_url():
    return settings.LOGIN_URL


@register.simple_tag
def get_settings(settings_parameter):
    return getattr(settings, settings_parameter)


@register.inclusion_tag('utils/IMPORTS.html')
def render_imports():
    return {'offline_imports': settings.COMMENT_OFFLINE_IMPORTS}


@register.simple_tag
def get_profile_image(user):
    if settings.COMMENT_PROFILE_IMAGE_FIELD:
        profile = getattr(user, settings.COMMENT_PROFILE_IMAGE_FIELD)
        if profile:
            return profile.url
        else:
            return static(settings.COMMENT_PROFILE_IMAGE_DEFAULT)
    else:
        return None
