from .models import User, Follow
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from blogs.models import Blog


class UserRegisterSerializer(ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError("passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "address",
        ]


class UserBriefSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile_picture"]


class BlogBriefSerializer(ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "cover_image",
            "likes",
            "like_count",
            "comment_count",
            "content",
            "status",
            "created_at",
        ]

    def get_like_count(self, obj):
        return obj.likes.filter(is_liked=True).count()

    def get_comment_count(self, obj):
        return obj.comments.count()


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "is_followed", "created_at"]
        read_only_fields = ["id", "created_at", "follower"]


class UserDetailSerializer(ModelSerializer):
    blogs = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "address",
            "detail",
            "blogs",
            "follower_count",
            "following_count",
            "is_followed",
        ]

    def get_follower_count(self, obj):
        return obj.follower.count()

    def get_following_count(self, obj):
        return obj.following.filter(is_followed=True).count()

    def get_is_followed(self, obj):
        request = self.context["request"]
        return obj.following.filter(is_followed=True, follower=request.user).exists()

    def get_blogs(self, obj):
        from blogs.serializers import (
            BlogSerializer,
        )  # ✅ lazy import here, inside method

        blogs = obj.blog_created_by.all()
        return BlogSerializer(blogs, many=True).data
