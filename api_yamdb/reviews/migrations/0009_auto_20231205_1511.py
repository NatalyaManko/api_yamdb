# Generated by Django 3.2 on 2023-12-05 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_auto_20231205_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genres',
        ),
        migrations.AddField(
            model_name='title',
            name='genres',
            field=models.ManyToManyField(to='reviews.Genre', verbose_name='Жанры произведений'),
        ),
    ]