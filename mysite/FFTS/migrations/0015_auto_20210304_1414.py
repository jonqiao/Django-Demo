# Generated by Django 3.1.7 on 2021-03-04 06:14

from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('FFTS', '0014_auto_20210304_0321'),
  ]

  operations = [
    migrations.AlterField(
      model_name='project',
      name='ffts_id',
      field=models.CharField(default='Auto-Generation', help_text='Use AUTO value or input your own value!', max_length=47, verbose_name='FFTS ID'),
    ),
  ]
