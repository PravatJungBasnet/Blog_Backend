from .models import Blog, Like, Comment, Bookmark
from core.serializers import BaseSerializer
from users.serializers import UserBriefSerializer
from rest_framework import serializers


class BlogSerializer(BaseSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "cover_image",
            "content",
            "status",
            "like_count",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "slug",
        ]
        serialize_fields = {
            "created_by": UserBriefSerializer,
            "updated_by": UserBriefSerializer,
        }

    def get_like_count(self, obj):
        return obj.like_set.count()


class LikeSerializer(BaseSerializer):
    class Meta:
        model = Like
        fields = ["id", "blog", "user", "is_liked", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class CommentSerializer(BaseSerializer):
    class Meta:
        model = Comment
        fields = ["id", "blog", "user", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class BookMarkSerializer(BaseSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "blog", "user", "is_bookmarked", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
