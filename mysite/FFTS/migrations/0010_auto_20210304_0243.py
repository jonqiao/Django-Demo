# Generated by Django 3.1.7 on 2021-03-03 18:43

from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('FFTS', '0009_auto_20210304_0238'),
  ]

  operations = [
    migrations.AlterField(
      model_name='project',
      name='business_flow',
      field=models.CharField(help_text='e.g.: BU_SRC_TO_DEST_UAT', max_length=32, verbose_name='Business Flow'),
    ),
    migrations.AlterField(
      model_name='project',
      name='ffts_id',
      field=models.CharField(max_length=47, verbose_name='FFTS ID'),
    ),
  ]
