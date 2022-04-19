from rest_framework import serializers
from django.shortcuts import get_object_or_404
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


class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ('nested_level',)

    def create(self, validated_data):
        new_comment = Comment.objects.create(**validated_data)
        main_comment_id = self.context['request'].query_params.get(
            'comment_id'
        )
        if main_comment_id is not None:
            main_comment = get_object_or_404(
                Comment,
                pk=main_comment_id
            )
            NestedComment.objects.create(
                main_comment=main_comment,
                nested_comment=new_comment
            )
            new_comment(nested_level=main_comment.nested_level + 1)
            new_comment.save()
        return new_comment


class ReadCommentSerializer(serializers.ModelSerializer):
    main_comment = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'pk'
            'text',
            'author',
            'article',
            'nested_level',
            'main_comment'
        )

    def get_main_comment(self, obj):
        if NestedComment.objects.get(nested_comment=obj).exists():
            return NestedComment.objects.get(
                nested_comment=obj
            ).main_comment.pk
        return None


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        exclude = ('author',)


class ReadArticleSerializer(serializers.ModelSerializer):
    author = ReadUserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
