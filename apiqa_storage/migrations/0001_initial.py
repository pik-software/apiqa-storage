# Generated by Django 2.2.2 on 2019-06-11 12:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('path', models.CharField(max_length=512, verbose_name='Путь')),
                ('size', models.BigIntegerField(verbose_name='Размер')),
                ('bucket_name', models.CharField(default='test-bucket', max_length=255)),
                ('content_type', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Вложение',
                'verbose_name_plural': 'Вложения',
            },
        ),
    ]
