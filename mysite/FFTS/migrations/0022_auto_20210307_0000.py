# Generated by Django 3.1.7 on 2021-03-06 16:00

from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('FFTS', '0021_auto_20210305_2321'),
  ]

  operations = [
    migrations.RemoveField(
      model_name='project',
      name='source_array',
    ),
    migrations.RemoveField(
      model_name='project',
      name='source_dir',
    ),
    migrations.RemoveField(
      model_name='project',
      name='support_team_email',
    ),
    migrations.AddField(
      model_name='project',
      name='app_support_callout',
      field=models.CharField(choices=[('BHO', 'BHO'), ('7x24', '7x24'), ('TICKET', 'TICKET')], default='TICKET', max_length=6,
                             verbose_name='app.support.callout'),
    ),
    migrations.AddField(
      model_name='project',
      name='app_support_team',
      field=models.CharField(default='PLEASE-SUPPRESS-INCIDENT', max_length=128, verbose_name='app.support.team'),
    ),
    migrations.AddField(
      model_name='project',
      name='app_support_team_email_id',
      field=models.CharField(default='null', max_length=256, verbose_name='app.support.team.email.id'),
    ),
    migrations.AddField(
      model_name='project',
      name='long_retry_email',
      field=models.CharField(default='null', max_length=256, verbose_name='long.retry.email'),
    ),
    migrations.AddField(
      model_name='project',
      name='project_desc',
      field=models.CharField(default='null', max_length=256, verbose_name='project.desc'),
    ),
    migrations.AddField(
      model_name='project',
      name='short_retry_failure_email',
      field=models.CharField(default='null', max_length=256, verbose_name='short.retry.failure.email'),
    ),
    migrations.AddField(
      model_name='project',
      name='source_folder',
      field=models.CharField(default='null', max_length=256, verbose_name='source.folder'),
    ),
    migrations.AddField(
      model_name='project',
      name='source_resource',
      field=models.CharField(default='null', max_length=1024, verbose_name='source.resource'),
    ),
    migrations.AlterField(
      model_name='project',
      name='business_flow',
      field=models.CharField(help_text='e.g.: BU_SRC_TO_DEST_UAT', max_length=38, verbose_name='Business Flow'),
    ),
    migrations.AlterField(
      model_name='project',
      name='dest_array',
      field=models.CharField(default='null', max_length=1024, verbose_name='dest.array'),
    ),
    migrations.AlterField(
      model_name='project',
      name='ffts_id',
      field=models.CharField(default='Auto-Generation', max_length=50, unique=True, verbose_name='FFTS ID'),
    ),
    migrations.AlterField(
      model_name='project',
      name='strategy',
      field=models.CharField(choices=[('Polling', 'Polling'), ('Trigger', 'Trigger'), ('Initialization', 'Initialization')], max_length=15,
                             verbose_name='Strategy'),
    ),
  ]
