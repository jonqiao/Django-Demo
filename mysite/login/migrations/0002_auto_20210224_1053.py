# Generated by Django 3.1.7 on 2021-02-24 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='pwd',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='user',
            new_name='username',
        ),
    ]
