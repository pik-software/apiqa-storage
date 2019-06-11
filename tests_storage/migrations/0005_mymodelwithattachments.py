# Generated by Django 2.2.2 on 2019-06-11 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiqa_storage', '0001_initial'),
        ('tests_storage', '0004_auto_20190530_0945'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModelWithAttachments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachments', models.ManyToManyField(to='apiqa_storage.Attachment', verbose_name='Вложения')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]