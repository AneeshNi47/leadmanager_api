from rest_framework import routers
from .api import QRCodeViewSet, QRCodeTypeViewSet


router = routers.DefaultRouter()
router.register('api/qr-code-types', QRCodeTypeViewSet, 'qr-code-type')
router.register('api/qr-codes', QRCodeViewSet, 'qr-codes')

urlpatterns = router.urls