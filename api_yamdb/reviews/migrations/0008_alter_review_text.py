# Generated by Django 3.2 on 2023-11-29 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20231129_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(max_length=200, verbose_name='Текст'),
        ),
    ]
