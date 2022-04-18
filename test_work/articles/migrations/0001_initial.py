# Generated by Django 3.1.14 on 2022-04-18 19:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название статьи')),
                ('text', models.TextField(verbose_name='Текст статьи')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания статьи')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='Автор статьи')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='articles.article', verbose_name='Статья')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='NestingComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nested_level', models.PositiveIntegerField(verbose_name='Уровень вложенности комментария')),
                ('main_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_comments', to='articles.comment', verbose_name='Основной комментарий')),
                ('nested_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nested_comments', to='articles.comment', verbose_name='Вложенный комментарий')),
            ],
            options={
                'verbose_name': 'Вложенные комментарий',
                'verbose_name_plural': 'Вложенные комментарии',
            },
        ),
    ]
