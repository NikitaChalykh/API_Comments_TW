from django.contrib import admin

from .models import Article, Comment, NestingComment


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'text',
        'pub_date'
    )
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'article',
        'text',
        'nested_level'
    )
    list_filter = ('author', 'article')
    empty_value_display = '-пусто-'


class NestingCommentAdmin(admin.ModelAdmin):
    list_display = (
        'main_comment',
        'nested_comment',
    )
    list_filter = ('main_comment',)
    empty_value_display = '-пусто-'


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(NestingComment, NestingCommentAdmin)
