from rest_framework.routers import DefaultRouter
from apps.tenant import views

router = DefaultRouter()
router.register('tenants', views.TenantViewSet)
urlpatterns = router.get_urls()
