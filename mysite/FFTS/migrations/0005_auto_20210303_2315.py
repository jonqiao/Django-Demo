# Generated by Django 3.1.7 on 2021-03-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('FFTS', '0004_auto_20210303_2307'),
  ]

  operations = [
    migrations.AlterField(
      model_name='project',
      name='ffts_id',
      field=models.CharField(help_text='e.g.: BU_SRC_TO_DEST_UAT', max_length=128, verbose_name='FFTS ID'),
    ),
  ]
