from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("studies", views.StudyViewSet, basename="study")

urlpatterns = router.urls
