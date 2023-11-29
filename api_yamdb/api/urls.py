from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'titles/(?P<title_pk>\d+)/reviews',
                ReviewViewSet,
                basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),
]
