from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Article(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название статьи'
    )
    text = models.TextField(
        verbose_name='Текст статьи'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Автор статьи'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания статьи'
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.name[:15]


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Статья'
    )
    main_comment = models.ForeignKey(
        'self',
        null=True,
        on_delete=models.CASCADE,
        related_name='nested_comments',
        verbose_name='Основной комментарий'
    )
    nested_level = models.PositiveIntegerField(
        # 0 - комментарий относится к статье
        # 1,2,3 и т.д. - уровень вложенности для вложенного комментария
        default=0,
        verbose_name='Уровень вложенности комментария'
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
