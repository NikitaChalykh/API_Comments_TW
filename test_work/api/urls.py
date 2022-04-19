from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from .views import ArticleViewSet, CommentViewSet, UserViewSet

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('articles', ArticleViewSet)
router_api.register(
    r'^articles/(?P<article_id>\d+)/comments',
    CommentViewSet,
    basename='article_comments'
)
router_api.register(
    r'^articles/(?P<article_id>\d+)/comments/(?P<comment_id>\d+)/nested',
    CommentViewSet,
    basename='nested_comments'
)
router_api.register('users', UserViewSet)

urlpatterns = [
    path('auth/token/login/', TokenCreateView.as_view(), name='token_login'),
    path(
        'auth/token/logout/', TokenDestroyView.as_view(), name='token_logout'
    ),
    path('', include(router_api.urls))
]
