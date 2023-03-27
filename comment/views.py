from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from comment.forms import CommentForm
from comment.mixins import CommentMixin
from comment.models import Comment, Reaction, React, CommentSettings


class CommentDetail(TemplateView):
    template_name = 'comment/comment/comment_body.html'

    def get(self, request, *args, **kwargs):
        urlhash = request.GET.get('urlhash')
        settings_slug = request.GET.get('settings_slug')
        context = {
            'comment': Comment.objects.get(urlhash=urlhash),
            'settings': CommentSettings.objects.get(slug=settings_slug)
        }
        return render(request, self.template_name, context=context)


class CommentList(ListView):
    context_object_name = 'comments'
    template_name = 'comment/comment/comment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings_slug = self.request.GET.get('settings_slug')
        context['settings'] = CommentSettings.objects.get(slug=settings_slug)
        return context

    def get_queryset(self):
        queryset = None
        if self.request.GET:
            app_name = self.request.GET.get('app_name')
            model_name = self.request.GET.get('model_name')
            object_id = self.request.GET.get('object_id')
            settings_slug = self.request.GET.get('settings_slug')
            comment_settings = CommentSettings.objects.get(slug=settings_slug)
            content_type = ContentType.objects.get(app_label=app_name, model=model_name.lower())
            queryset = Comment.objects.filter(content_type=content_type, object_id=object_id)
            queryset = queryset.filter_accepted().filter_parents()
            queryset = queryset.order_pinned_newest()

            # Pagination
            page = self.request.GET.get('page', 1)
            if comment_settings.per_page == 0:
                paginator = Paginator(queryset, queryset.count())
            else:
                paginator = Paginator(queryset, comment_settings.per_page)
            try:
                queryset = paginator.page(page)
            except PageNotAnInteger:
                queryset = paginator.page(1)
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages)

        return queryset


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
            settings_slug = request.POST.get('settings_slug', None)
            comment_settings = CommentSettings.objects.get(slug=settings_slug)
            time_posted = timezone.now()
            comment.content_type = ContentType.objects.get(app_label=app_name, model=model_name.lower())
            comment.object_id = object_id

            if parent_id:
                parent_comment = Comment.objects.get(urlhash=parent_id)
                comment.parent = parent_comment
            else:
                comment.parent = None
            comment.posted = time_posted

            if not comment_settings.status_check:
                comment.status = 'a'

            comment.save()
            return HttpResponse(status=200)
        else:
            return HttpResponseBadRequest()


class CommentUpdate(CommentMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'urlhash': self.object.urlhash}, status=200)

    def form_invalid(self, form):
        super().form_invalid(form)
        return HttpResponseBadRequest()


class CommentDelete(CommentMixin, View):
    def get(self, request, urlhash, *args, **kwargs):
        return render(request, 'comment/forms/comment_form_delete.html', context={'urlhash': urlhash})

    def post(self, request, urlhash, *args, **kwargs):
        comment = Comment.objects.get(urlhash=urlhash)
        if comment:
            comment.delete()
            return HttpResponse(status=200)
        return HttpResponseBadRequest()


class CommentReact(CommentMixin, View):
    def get(self, request, *args, **kwargs):
        urlhash = request.GET.get('urlhash')
        context = {'comment': Comment.objects.get(urlhash=urlhash)}
        return render(request, 'comment/comment/comment_reactions.html', context=context)

    def post(self, request, *args, **kwargs):
        user = request.user
        comment_urlhash = request.POST.get('urlhash', None)
        react_slug = request.POST.get('react_slug', None)

        reaction = Reaction.objects.filter(user=user, comment__urlhash=comment_urlhash).first()

        if reaction:  # Update Previous Reaction
            if reaction.react.slug == react_slug:  # Delete Previous Reaction
                reaction.delete()
            else:  # Change Previous Reaction
                react = React.objects.get(slug=react_slug)
                reaction.react = react
                reaction.save()
        else:  # Create New Reaction
            comment = Comment.objects.get(urlhash=comment_urlhash)
            react = React.objects.get(slug=react_slug)
            Reaction.objects.create(user=user, comment=comment, react=react)

        return HttpResponse(status=200)
