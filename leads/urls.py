from rest_framework import routers
from .api import LeadViewSet, LeadStatusViewSet


router = routers.DefaultRouter()
router.register('api/leads', LeadViewSet, 'leads')
router.register('api/lead_status', LeadStatusViewSet, 'leads_status')

urlpatterns = router.urls