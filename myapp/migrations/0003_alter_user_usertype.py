# Generated by Django 4.2.7 on 2023-11-23 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_user_usertype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='usertype',
            field=models.CharField(default='rider', max_length=100),
        ),
    ]