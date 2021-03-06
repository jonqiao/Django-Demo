# Generated by Django 3.1.7 on 2021-02-28 02:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('polls', '0001_initial'),
  ]

  operations = [
    migrations.AddField(
      model_name='choice',
      name='CREATED_BY',
      field=models.CharField(default='Jon', max_length=32, verbose_name='created_by'),
      preserve_default=False,
    ),
    migrations.AddField(
      model_name='choice',
      name='CREATED_TIME',
      field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created_ts'),
      preserve_default=False,
    ),
    migrations.AddField(
      model_name='choice',
      name='UPDATED_BY',
      field=models.CharField(default='Jon', max_length=32, verbose_name='updated_by'),
      preserve_default=False,
    ),
    migrations.AddField(
      model_name='choice',
      name='UPDATED_TIME',
      field=models.DateTimeField(auto_now=True, verbose_name='updated_ts'),
    ),
    migrations.AddField(
      model_name='question',
      name='CREATED_BY',
      field=models.CharField(default='Jon', max_length=32, verbose_name='created_by'),
      preserve_default=False,
    ),
    migrations.AddField(
      model_name='question',
      name='CREATED_TIME',
      field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created_ts'),
      preserve_default=False,
    ),
    migrations.AddField(
      model_name='question',
      name='UPDATED_BY',
      field=models.CharField(default=django.utils.timezone.now, max_length=32, verbose_name='updated_by'),
      preserve_default=False,
    ),
    migrations.AddField(
      model_name='question',
      name='UPDATED_TIME',
      field=models.DateTimeField(auto_now=True, verbose_name='updated_ts'),
    ),
  ]
