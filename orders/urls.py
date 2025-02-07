from django.urls import include, path
from .views import order_list, order_create, order_delete, order_update, revenue_report
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'api/orders', OrderViewSet)

urlpatterns = [
    path('', order_list, name='order_list'),
    path('create/', order_create, name='order_create'),
    path('delete/<int:order_id>/', order_delete, name='order_delete'),
    path('update/<int:order_id>/', order_update, name='order_update'),
    path('revenue/', revenue_report, name='revenue_report'),
    path('api/', include(router.urls)),
]