from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class CommentMixin(LoginRequiredMixin):
    def has_object_permission(self, obj):
        return True if obj.user == self.request.user else False

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if self.has_object_permission(obj):
            return obj
        else:
            raise PermissionDenied("Access Denied : update or delete comment.")
