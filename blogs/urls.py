from .views import BlogViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
app_name = "blogs"
router.register("", BlogViewset, basename="blogs")
urlpatterns = router.urls
