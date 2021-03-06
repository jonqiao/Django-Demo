# Generated by Django 3.1.7 on 2021-03-05 15:21

from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('FFTS', '0020_auto_20210305_1123'),
  ]

  operations = [
    migrations.AlterField(
      model_name='project',
      name='dest_array',
      field=models.CharField(default='null', max_length=1024, verbose_name='Destination'),
    ),
    migrations.AlterField(
      model_name='project',
      name='strategy',
      field=models.CharField(choices=[('Polling', 'Polling'), ('Trigger', 'Trigger'), ('Initialization', 'Initialization')], default='Trigger', max_length=15,
                             verbose_name='Strategy'),
    ),
    migrations.AlterField(
      model_name='project',
      name='support_team_email',
      field=models.CharField(default='null', max_length=256, verbose_name='support team email'),
    ),
  ]
