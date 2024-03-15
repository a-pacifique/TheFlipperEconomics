# Generated by Django 4.2.4 on 2024-03-07 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Articles', '0002_article_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date_written'], 'verbose_name': 'article', 'verbose_name_plural': 'articles'},
        ),
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.BooleanField(default=False, verbose_name='published'),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='article content'),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_written',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date written'),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(upload_to='articles/images/', verbose_name='article image'),
        ),
        migrations.AlterField(
            model_name='article',
            name='views',
            field=models.IntegerField(default=0, verbose_name='views'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='last name'),
        ),
    ]
