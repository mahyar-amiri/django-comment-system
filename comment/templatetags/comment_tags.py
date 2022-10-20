from django import template
from django.contrib.contenttypes.models import ContentType

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
