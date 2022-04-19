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
    serializer_class = UserSerializer
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
    serializer_class = ArticleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (CustomPermission,)

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
    viewsets.GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = None
    permission_classes = (CustomPermission,)

    # def perform_create(self, serializer):
    #     title_id = self.kwargs.get('title_id')
    #     title = get_object_or_404(Title, id=title_id)
    #     review_id = self.kwargs.get('review_id')
    #     review = get_object_or_404(Review, id=review_id, title=title)
    #     serializer.save(author=self.request.user, review=review)


class CommentViewSet(
    ArticleCommentViewSet,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin
):
    pass
