from rest_framework import viewsets

from articles.models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer


class ArticleViewSet(viewsets.ViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CommentViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
