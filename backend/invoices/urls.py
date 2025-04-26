from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, InvoiceCommentViewSet

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'comments', InvoiceCommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
] 