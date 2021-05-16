# Generated by Django 3.0.5 on 2021-05-16 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('webApp', '0012_remove_book_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('firstId', models.CharField(max_length=5, null=True)),
                ('secondId', models.CharField(max_length=5, null=True)),
                ('thirdId', models.CharField(max_length=5, null=True)),
                ('fourthId', models.CharField(max_length=5, null=True)),
                ('fifthId', models.CharField(max_length=5, null=True)),
            ],
        ),
    ]
