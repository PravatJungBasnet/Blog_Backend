from .views import BlogViewset, BookmarkView, LikeView, CommentViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
app_name = "blogs"
router.register("", BlogViewset, basename="blogs")

urlpatterns = [
    path("<str:slug>/like/", LikeView.as_view(), name="like"),
    path(
        "<str:slug>/comments/",
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
    path("<str:slug>/bookmark/", BookmarkView.as_view(), name="bookmark"),
]
urlpatterns += router.urls
