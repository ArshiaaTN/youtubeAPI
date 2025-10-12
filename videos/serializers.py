from rest_framework import serializers
from .models import Video, Like, Comment


class VideoSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'duration', 'video_url', 'views', 'likes_count', 'comments_count',
                  'is_liked_by_user']
        read_only_fields = ['id', 'views', 'likes_count', 'comments_count', 'is_liked_by_user']

    def get_likes_count(self, obj):
        return obj.get_likes_count()

    def get_comments_count(self, obj):
        return obj.get_comments_count()

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, video=obj).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    video_id = serializers.IntegerField(source='video.id', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'video_id', 'text', 'created_at']
        read_only_fields = ['id', 'username', 'video_id', 'created_at']

class VideoWatchSerializer(serializers.Serializer):
    quality = serializers.CharField(read_only=True)
    video_url = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)