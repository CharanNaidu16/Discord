# Generated by Django 5.1.4 on 2025-01-03 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discord_app', '0008_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
    ]