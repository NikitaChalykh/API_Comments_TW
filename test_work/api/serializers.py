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
    # нужно тут предусмотреть ссылку на главные комментарии
    nested_level = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'   


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        exclude  = ('author',)

        
class ReadArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

        
class RetrieveArticleSerializer(serializers.ModelSerializer):
    # нужно тут предусмотреть ссылку на главные комментарии
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = '__all__'
     
    def get_comments(self, obj):
        comments = obj.comments.filter(nested_level__regex='0|1|2|3')
        serializer = CommentSerializer(comments, many=True)
        return serializer.data
