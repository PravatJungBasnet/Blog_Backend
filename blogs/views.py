from .serializers import BlogSerializer, LikeSerializer
from .models import Blog, Like
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
        blog_id = self.kwargs.get("blog_id")
        print(blog_id)
        return Like.objects.filter(
            blog_id=blog_id,
        ).select_related("user")

    def create(self, request, *args, **kwargs):
        blog_id = self.kwargs.get("blog_id")
        blog = get_object_or_404(Blog, id=blog_id)

        like, created = Like.objects.get_or_create(blog=blog, user=request.user)
        if not created:
            like.is_liked = not like.is_liked
            like.save(update_fields=["is_liked", "updated_at"])

        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_200_OK)
