# Generated by Django 5.1.4 on 2025-01-03 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discord_app', '0009_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='user.png', null=True, upload_to=''),
        ),
    ]
