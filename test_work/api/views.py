from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from articles.models import Article, Comment, User

from .permissions import CustomPermission
from .serializers import (ArticleSerializer, CommentSerializer,
                          UserSerializer, ReadUserSerializer)


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
        return ReadUserSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['GET']
    )
    def show_comments(self, request):
        # тут будет код для показа комментов стаитья до 3 уровня
        # вложенности
        pass


class ArticleCommentViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = None
    permission_classes = (CustomPermission,)

    def perform_create(self, serializer):
        # описать тут сохранение комментария к статье
        pass

    def perform_destroy(self, serializer):
        # описать тут удаления комментария к статье и еще всех вложенных
        pass


class NestedCommentViewSet(ArticleCommentViewSet, mixins.ListModelMixin):

    def perform_create(self, serializer):
        # описать тут сохранение вложенного комментария
        pass

    def perform_destroy(self, serializer):
        # описать тут удаления вложенного комментария и еще всех вложенных
        pass
