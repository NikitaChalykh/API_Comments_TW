from django.urls import include, path
from rest_framework import routers

from .views import ArticleViewSet, CommentViewSet

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('comments', ArticleViewSet)
router_api.register('articles', CommentViewSet)

urlpatterns = [
    path('', include(router_api.urls))
]
