from customers.views import CustomerViewSet
from rest_framework.routers import DefaultRouter

app_name = 'customers'

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = router.urls
