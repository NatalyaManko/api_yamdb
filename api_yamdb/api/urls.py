from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenresViewSet, TitlesViewSet

router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet, 'categories')
router_v1.register('genres', GenresViewSet, 'genres')
router_v1.register('titles', TitlesViewSet, 'titles')

urlpatterns = [
    path('v1/', include(router_v1.urls),)
]