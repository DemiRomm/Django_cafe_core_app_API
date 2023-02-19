from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import Menu, MealType


router = DefaultRouter(trailing_slash=False)
router.register(r'menu', Menu, basename='menu')
router.register(r'meal_category', MealType, basename='meal_category')
urlpatterns = router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)