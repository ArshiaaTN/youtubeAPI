from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Video, Like, Comment
from .serializers import VideoSerializer, CommentSerializer, VideoWatchSerializer
from subscriptions.models import Subscription
from history.models import History
from datetime import datetime


class VideoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "Only admins can create videos"}, status=status.HTTP_403_FORBIDDEN)

        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Video created successfully",
                "video": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return None

    def get(self, request, pk):
        video = self.get_object(pk)
        if not video:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Only admins can update videos"}, status=status.HTTP_403_FORBIDDEN)

        video = self.get_object(pk)
        if not video:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Video updated successfully",
                "video": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Only admins can delete videos"}, status=status.HTTP_403_FORBIDDEN)

        video = self.get_object(pk)
        if not video:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        video.delete()
        return Response({"message": "Video deleted successfully"}, status=status.HTTP_200_OK)


class VideoWatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        subscription = Subscription.objects.filter(user=request.user, is_active=True).first()

        if not subscription:
            return Response({"error": "You need an active subscription to watch videos"},
                            status=status.HTTP_403_FORBIDDEN)

        quality_map = {
            'Basic': '480p',
            'Premium': '720p',
            'VIP': '1080p'
        }
        quality = quality_map.get(subscription.type, '480p')

        video.views += 1
        video.save()

        History.objects.create(
            user=request.user,
            video=video,
            watch_date=datetime.now().date(),
            duration=video.duration
        )

        return Response({
            "message": "Video is now playing",
            "video": {
                "id": video.id,
                "title": video.title,
                "description": video.description,
                "video_url": video.video_url,
                "quality": quality,
                "duration": str(video.duration)
            },
            "subscription_type": subscription.type
        }, status=status.HTTP_200_OK)


class VideoLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, video=video)

        if not created:
            return Response({"message": "You already liked this video"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Video liked successfully",
            "likes_count": video.get_likes_count()
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            like = Like.objects.get(user=request.user, video=video)
            like.delete()
            return Response({
                "message": "Like removed successfully",
                "likes_count": video.get_likes_count()
            }, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"error": "You haven't liked this video"}, status=status.HTTP_400_BAD_REQUEST)


class VideoCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(video=video)
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "video_id": video.id,
            "video_title": video.title,
            "comments_count": comments.count(),
            "comments": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, video=video)
            return Response({
                "message": "Comment added successfully",
                "comment": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "video_id": video.id,
            "title": video.title,
            "views": video.views,
            "likes": video.get_likes_count(),
            "comments": video.get_comments_count()
        }, status=status.HTTP_200_OK)