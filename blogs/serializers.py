from .models import Blog
from core.serializers import BaseSerializer
from users.serializers import UserBriefSerializer


class BlogSerializer(BaseSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "cover_image",
            "content",
            "status",
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
