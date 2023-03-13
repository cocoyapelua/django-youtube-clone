from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, DeleteView, UpdateView
from django.views.generic.edit import CreateView

from .forms import CommentForm
from .models import Video, History
from .utils import get_actual_date, get_popular_videos


# Video views
class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'description', 'video']
    template_name = 'video/video_create.html'
    success_url = reverse_lazy('video_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class VideoDetailView(View):

    def get(self, request, *args, **kwargs):
        video = get_object_or_404(Video, video=kwargs['pk'])

        if kwargs.get('like'):
            Video.save_like(video, request.user, kwargs['like'])
            return redirect('video_detail', pk=video.video)

        Video.save_history(video, request.user, get_actual_date())
        return render(request, 'video/video_detail.html', {'video': video, 'form': CommentForm()})

    def post(self, request, *args, **kwargs):
        video = get_object_or_404(Video, video=kwargs['pk'])
        Video.save_history(video, request.user, get_actual_date())

        comment_form = CommentForm(request.POST)
        if self.request.user.is_authenticated:
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.video = video
                comment.comment = comment_form.cleaned_data['comment']
                comment.user = request.user
                comment.save()
                return redirect('video_detail', pk=video.video)

        return render(request, 'video/video_detail.html', {'video': video, 'form': CommentForm()})


class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['title', 'description', 'video']
    template_name = 'video/video_update.html'

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.user

    def get_object(self, queryset=None):
        return Video.objects.get(video=self.kwargs['pk'])


class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'video/video_delete.html'
    success_url = reverse_lazy('video_list')

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.user

    def get_object(self, queryset=None):
        return Video.objects.get(video=self.kwargs['pk'])


class VideoListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Video
    template_name = 'video/video_list.html'
    context_object_name = 'videos'

    def get_queryset(self):
        return Video.objects.filter(user=self.request.user).order_by('-date')


class VideoPopularView(TemplateView):
    template_name = 'video/video_popular.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        videos = Video.objects.all().order_by('-date')
        context['popular_videos'] = get_popular_videos(videos)
        return context


# History views
class HistoryListView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'video/video_history.html'
    context_object_name = 'videos'
    paginate_by = 10

    def get_queryset(self):
        return History.objects.select_related('video').filter(user=self.request.user).order_by('-date')
