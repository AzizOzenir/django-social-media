# Generated by Django 4.2.2 on 2023-07-21 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_post_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
    ]
