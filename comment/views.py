from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.contenttypes.models import ContentType

from comment.mixins import CommentMixin
from comment.models import Comment
from comment.forms import CommentForm
from comment import settings


class CommentList(ListView):
    context_object_name = 'comments'
    template_name = 'comment/comment_list.html'

    def get_queryset(self):
        queryset = None
        if self.request.GET:
            app_name = self.request.GET.get('app_name')
            model_name = self.request.GET.get('model_name')
            object_id = self.request.GET.get('object_id')
            content_type = ContentType.objects.get(app_label=app_name, model=model_name.lower())
            queryset = Comment.objects.filter(content_type=content_type, object_id=object_id)
            queryset = queryset.filter_accepted().filter_parents()
            queryset = queryset.order_newest()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CommentList, self).get_context_data(**kwargs)
        context['settings'] = {
            'COMMENT_ALLOW_SPOILER': settings.COMMENT_ALLOW_SPOILER,
            'COMMENT_ALLOW_REPLY': settings.COMMENT_ALLOW_REPLY,
            'COMMENT_ALLOW_EDIT': settings.COMMENT_ALLOW_EDIT,
            'COMMENT_ALLOW_DELETE': settings.COMMENT_ALLOW_DELETE,
        }
        return context


class CommentCreate(CommentMixin, CreateView):
    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)

            comment.user = request.user
            app_name = request.POST.get('app_name', None)
            model_name = request.POST.get('model_name', None)
            object_id = request.POST.get('object_id', None)
            parent_id = request.POST.get('parent_id', None)
            time_posted = timezone.now()
            comment.content_type = ContentType.objects.get(app_label=app_name, model=model_name.lower())
            comment.object_id = object_id

            if parent_id:
                parent_comment = Comment.objects.get(urlhash=parent_id)
                comment.parent = parent_comment
            else:
                comment.parent = None
            comment.posted = time_posted

            if not settings.COMMENT_STATUS_CHECK:
                comment.status = 'a'

            comment.save()
            return JsonResponse({'result': 'success'}, status=200)
        return JsonResponse({'result': 'fail'})


class CommentUpdate(CommentMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'result': 'success'}, status=200)


class CommentDelete(CommentMixin, TemplateView):
    def get(self, request, urlhash, *args, **kwargs):
        return render(request, 'forms/comment_form_delete.html', context={'urlhash': urlhash})

    def post(self, request, urlhash, *args, **kwargs):
        comment = Comment.objects.get(urlhash=urlhash)
        if comment:
            comment.delete()
            return JsonResponse({'result': 'success'}, status=200)
        return JsonResponse({'result': f'fail'})
