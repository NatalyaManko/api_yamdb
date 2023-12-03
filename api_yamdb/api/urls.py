from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import APIGetToken, APISignup, MeViewSet, UsersViewSet

router = SimpleRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/users/me/', MeViewSet, name='me'),
    path('v1/', include(router.urls)),
]
