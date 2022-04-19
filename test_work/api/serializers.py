from django.shortcuts import get_object_or_404
from rest_framework import serializers

from articles.models import Article, Comment, NestedComment, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'first_name',
            'last_name',
            'email'
        )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Username указан неверно!')
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ReadUserSerializer(serializers.ModelSerializer):
    '''Добавлен сериализатор на чтение для красивого отображения работы апи
    в редоке, можно было бы реализовать через словарь initial_data -
    но оставил такое решение'''
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        exclude = ('author',)


class ReadArticleSerializer(serializers.ModelSerializer):
    '''Как и в примере с юзерами, добавил сериалайзер только для чтения
    для более читабельного отображения в апи авторов'''
    author = ReadUserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ('nested_level', 'author', 'article')

    def create(self, validated_data):
        '''Если сериалайзер вызывается из CommentViewSet,
        то, ко всему прочему, будет создана новая запись
        в модели вложенных комментариев,
        новый комментарий также получит данные о вложенности
        для корректного построения дерева комментариев'''
        new_comment = Comment.objects.create(**validated_data)
        main_comment_id = self.context.get('view').kwargs.get('comment_id')
        if main_comment_id is not None:
            main_comment = get_object_or_404(
                Comment,
                pk=main_comment_id
            )
            NestedComment.objects.create(
                main_comment=main_comment,
                nested_comment=new_comment
            )
            new_comment.nested_level = main_comment.nested_level + 1
            new_comment.save()
        return new_comment


class ReadCommentSerializer(serializers.ModelSerializer):
    main_comment = serializers.SerializerMethodField()
    author = ReadUserSerializer(read_only=True)
    article = ReadArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'pk',
            'text',
            'author',
            'article',
            'nested_level',
            'main_comment'
        )

    def get_main_comment(self, obj):
        '''Необходимое поле для фронтенда для
        построения корректного дерева комментариев -
        данные о вложенности комментария'''
        if NestedComment.objects.filter(nested_comment=obj).exists():
            return NestedComment.objects.get(
                nested_comment=obj
            ).main_comment.pk
        return None
