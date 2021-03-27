# Generated by Django 3.1.7 on 2021-03-03 14:06

from django.db import migrations, models


class Migration(migrations.Migration):
  initial = True

  dependencies = [
  ]

  operations = [
    migrations.CreateModel(
      name='Project',
      fields=[
        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('CREATED_BY', models.CharField(max_length=32, verbose_name='CREATED_BY')),
        ('CREATED_TIME', models.DateTimeField(auto_now_add=True, verbose_name='CREATED_TIME')),
        ('UPDATED_BY', models.CharField(max_length=32, verbose_name='UPDATED_BY')),
        ('UPDATED_TIME', models.DateTimeField(auto_now=True, verbose_name='UPDATED_TIME')),
        ('ffts_id', models.CharField(help_text='e.g.: BU_SRC_TO_DEST_UAT', max_length=32, verbose_name='FFTS ID')),
        ('strategy', models.CharField(choices=[('Polling', 'Polling'), ('Trigger', 'Trigger')], max_length=32, verbose_name='Strategy')),
        ('config_sync', models.CharField(default='N', max_length=3, verbose_name='Config Sync?')),
        ('dest_array', models.CharField(max_length=1024, verbose_name='Destination')),
        ('support_team_email', models.CharField(max_length=256, verbose_name='support team email')),
        ('source_array', models.CharField(max_length=1024, verbose_name='Source')),
        ('source_dir', models.CharField(max_length=256, verbose_name='Source DIR')),
      ],
    ),
  ]
