# Generated by Django 3.1.7 on 2021-02-28 06:30

from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('polls', '0003_auto_20210228_1100'),
  ]

  operations = [
    migrations.AlterField(
      model_name='choice',
      name='choice_text',
      field=models.CharField(max_length=200, verbose_name='choice'),
    ),
    migrations.AlterField(
      model_name='question',
      name='question_text',
      field=models.CharField(max_length=200, verbose_name='question'),
    ),
  ]
