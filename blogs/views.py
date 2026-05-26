from .serializers import BlogSerializer
from .models import Blog
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


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
