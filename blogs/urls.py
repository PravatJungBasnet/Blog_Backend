from .views import BlogViewset, LikeView
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
app_name = "blogs"
router.register("", BlogViewset, basename="blogs")
urlpatterns = [path("<int:blog_id>/like/", LikeView.as_view(), name="like")]
urlpatterns += router.urls
