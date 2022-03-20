from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       AdminViewSet, APIGetJWTToken, APIUserData,
                       APIUserRegistration, ReviewViewSet, CommentViewSet)

router_v1 = SimpleRouter()
router = DefaultRouter()

app_name = 'api'

router.register('api/v1/users', AdminViewSet)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
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

urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
    path('api/v1/auth/signup/', APIUserRegistration.as_view()),
    path('api/v1/auth/token/', APIGetJWTToken.as_view()),
    path('api/v1/users/me/', APIUserData.as_view()),
    path('', include(router.urls)),
]
