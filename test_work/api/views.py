from rest_framework import viewsets

from articles.models import Article, Comment


class ArticleViewSet(viewsets.ViewSet):
    queryset = Article.objects.all()
    pass


class CommentViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    pass
