from django.shortcuts import get_object_or_404
from rest_framework import serializers

from articles.models import Article, Comment, User


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
        exclude = ('nested_level', 'author', 'article', 'main_comment')

    def create(self, validated_data):
        '''Если сериалайзер вызывается из CommentViewSet,
        то, ко всему прочему, новый комментарий
        также получит данные о вложенности
        для корректного построения дерева комментариев'''
        new_comment = Comment.objects.create(**validated_data)
        main_comment_id = self.context.get('view').kwargs.get('comment_id')
        if main_comment_id is not None:
            main_comment = get_object_or_404(
                Comment,
                pk=main_comment_id
            )
            new_comment.nested_level = main_comment.nested_level + 1
            new_comment.main_comment = main_comment_id
            new_comment.save()
        return new_comment


class ReadCommentSerializer(serializers.ModelSerializer):
    author = ReadUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
