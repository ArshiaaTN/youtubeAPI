from django.urls import path
from .views import (
    VideoListView,
    VideoDetailView,
    VideoWatchView,
    VideoLikeView,
    VideoCommentView,
    VideoStatsView
)

urlpatterns = [
    path('', VideoListView.as_view(), name='video-list'),
    path('<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('<int:pk>/watch/', VideoWatchView.as_view(), name='video-watch'),
    path('<int:pk>/like/', VideoLikeView.as_view(), name='video-like'),
    path('<int:pk>/comments/', VideoCommentView.as_view(), name='video-comments'),
    path('<int:pk>/stats/', VideoStatsView.as_view(), name='video-stats'),
]