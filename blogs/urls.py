from .views import BlogViewset, LikeView, CommentViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
app_name = "blogs"
router.register("", BlogViewset, basename="blogs")

urlpatterns = [
    path("<int:blog_id>/like/", LikeView.as_view(), name="like"),
    path(
        "<int:blog_id>/comments/",
        CommentViewSet.as_view(
            {
                "get": "list",
                "post": "create",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="comments",
    ),
]
urlpatterns += router.urls
