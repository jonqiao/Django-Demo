# Generated by Django 3.1.7 on 2021-03-03 19:21

from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('FFTS', '0013_auto_20210304_0315'),
  ]

  operations = [
    migrations.AlterField(
      model_name='project',
      name='ffts_id',
      field=models.CharField(default='Auto-Generation', help_text='DO NOT change default value during add!', max_length=47, verbose_name='FFTS ID'),
    ),
  ]
