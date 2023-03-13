from django.urls import path
from .views import VideoCreateView, VideoDetailView, VideoListView, HistoryListView, VideoPopularView

urlpatterns = [
    path('create/', VideoCreateView.as_view(), name='video_create'),
    path('detail/<str:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('detail/<str:pk>/<str:like>', VideoDetailView.as_view(), name='video_like'),
    path('list/', VideoListView.as_view(), name='video_list'),
    path('history/', HistoryListView.as_view(), name='history'),
    path('popular/', VideoPopularView.as_view(), name='popular'),
]