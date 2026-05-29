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
<<<<<<< HEAD


class BlogBriefSerializer(BaseSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title","slug", "cover_image", "content", "status", "created_at"]
=======
>>>>>>> 0c7046d7d91710052dee357ffc40b839e5d104f9
