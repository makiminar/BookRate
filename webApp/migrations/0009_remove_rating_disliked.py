# Generated by Django 3.0.5 on 2021-04-23 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0008_rating_disliked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='disliked',
        ),
    ]
