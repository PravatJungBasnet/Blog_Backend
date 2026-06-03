from .models import Blog, Like, Comment, Bookmark
from core.serializers import BaseSerializer
from users.serializers import UserBriefSerializer
from rest_framework import serializers


class LikeBriefSerializer(BaseSerializer):
    class Meta:
        model = Like
        fields = ["id", "is_liked", "created_by"]
        read_only_fields = ["id", "is_liked", "created_by"]
        serialize_fields = {"created_by": UserBriefSerializer}


class CommentBriefSerializer(BaseSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "updated_at", "created_by"]
        serialize_fields = {"created_by": UserBriefSerializer}


class BlogSerializer(BaseSerializer):
    like_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

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
            "comments_count",
            "likes",
            "comments",
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
            "likes",
            "slug",
            "comments",
        ]
        serialize_fields = {
            "created_by": UserBriefSerializer,
            "updated_by": UserBriefSerializer,
            "likes": LikeBriefSerializer,
            "comments": CommentBriefSerializer,
        }

    def get_like_count(self, obj):
        return obj.likes.filter(is_liked=True).count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class LikeSerializer(BaseSerializer):
    class Meta:
        model = Like
        fields = ["id", "blog", "is_liked", "created_by", "created_at", "updated_at"]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
        serialize_fields = {"created_by": UserBriefSerializer}


class CommentSerializer(BaseSerializer):
    class Meta:
        model = Comment
        fields = ["id", "blog", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class BookmarkSerializer(BaseSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "blog", "is_bookmarked", "created_at", "updated_at"]
        read_only_fields = ["id", "blog", "created_at", "updated_at"]
