# Generated by Django 3.1.7 on 2021-03-02 14:23

from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('polls', '0012_auto_20210301_0011'),
  ]

  operations = [
    migrations.AlterField(
      model_name='choice',
      name='choice_text',
      field=models.CharField(
        choices=[('BMW', 'BMW'), ('Mercedes Benz', 'Mercedes Benz'), ('AUDI', 'AUDI'), ('LEXUS', 'LEXUS'), ('Apple', 'Apple'), ('Grape', 'Grape'),
                 ('Orange', 'Orange')], help_text='please choice one...', max_length=200, verbose_name='choice'),
    ),
  ]
