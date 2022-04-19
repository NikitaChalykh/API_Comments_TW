from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from articles.models import Article, Comment, User

from .permissions import CustomPermission
from .serializers import (ArticleSerializer, CommentSerializer,
                          ReadArticleSerializer, ReadCommentSerializer,
                          ReadUserSerializer, UserSerializer)


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = ReadUserSerializer
    pagination_class = None

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return UserSerializer
        return ReadUserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ReadArticleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (CustomPermission,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return ArticleSerializer
        return ReadArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleCommentViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = ReadCommentSerializer
    pagination_class = None
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(
            Article,
            pk=article_id
        )
        new_queryset = Comment.objects.filter(
            article=article
        ).filter(nested_level__regex='0|1|2|3')
        return new_queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentSerializer
        return ReadCommentSerializer

    def perform_create(self, serializer):
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(
            Article,
            pk=article_id
        )
        serializer.save(article=article, author=self.request.user)


class CommentViewSet(ArticleCommentViewSet):

    def get_queryset(self):
        comment_id = self.kwargs.get("comment_id")
        main_comment = get_object_or_404(
            Comment,
            pk=comment_id
        )
        new_queryset = Comment.objects.filter(
            nested_comments__main_comment=main_comment
        )
        return new_queryset
