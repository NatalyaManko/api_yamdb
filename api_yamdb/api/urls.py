from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenresViewSet, TitlesViewSet, ReviewViewSet

router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet, 'categories')
router_v1.register('genres', GenresViewSet, 'genres')
router_v1.register('titles', TitlesViewSet, 'titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)


urlpatterns = [
    path('v1/', include(router_v1.urls),)
]