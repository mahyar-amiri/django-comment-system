from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm


class CreateComment(CreateView):

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

            comment.save()

        return redirect(reverse('blog:home'))


class UpdateComment(UpdateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('blog:home')


class DeleteComment(DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'
    success_url = reverse_lazy('blog:home')
