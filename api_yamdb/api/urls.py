from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (APIGetToken, APISignup,
                    MeViewSet, UsersViewSet,
                    CategoryViewSet, GenresViewSet,
                    TitlesViewSet, ReviewViewSet,
                    CommentViewSet)

router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet, 'categories')
router_v1.register('genres', GenresViewSet, 'genres')
router_v1.register('titles', TitlesViewSet, 'titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
]
