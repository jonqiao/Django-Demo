# Generated by Django 3.1.7 on 2021-02-28 15:54

from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('polls', '0009_auto_20210228_2346'),
  ]

  operations = [
    migrations.AlterField(
      model_name='choice',
      name='choice_text',
      field=models.CharField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], max_length=200, verbose_name='choice'),
    ),
  ]
