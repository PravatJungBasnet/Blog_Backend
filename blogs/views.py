from .serializers import (
    BlogSerializer,
    LikeSerializer,
    CommentSerializer,
    BookmarkSerializer,
)
from .models import Blog, Like, Comment, Bookmark
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class ContextMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context


class CustomModelViewSet(ContextMixin, ModelViewSet):
    pass


class BlogViewset(CustomModelViewSet):
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    lookup_field = "slug"


class LikeView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=slug)
        return Like.objects.filter(blog=blog)

    def create(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=slug)

        like, created = Like.objects.get_or_create(
            blog=blog, created_by=self.request.user
        )
        if not created:
            like.is_liked = not like.is_liked
            like.save(update_fields=["is_liked", "updated_at"])

        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(CustomModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=slug)
        return Comment.objects.filter(blog=blog)

    def create(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=slug)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(blog=blog, created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookmarkView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        user = self.request.user
        blog = get_object_or_404(Blog, slug=slug)
        return Bookmark.objects.filter(blog=blog, created_by=user)

    def create(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=slug)

        bookmark, created = Bookmark.objects.get_or_create(
            blog=blog, created_by=self.request.user
        )
        if not created:
            bookmark.is_bookmarked = not bookmark.is_bookmarked
            bookmark.save(update_fields=["is_bookmarked", "updated_at"])

        serializer = self.get_serializer(bookmark)
        return Response(serializer.data, status=status.HTTP_200_OK)
