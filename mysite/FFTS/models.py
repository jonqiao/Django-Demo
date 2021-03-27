from django.db import models


# Create your models here.
class Project(models.Model):
  CREATED_BY = models.CharField('CREATED_BY', max_length=32)
  CREATED_TIME = models.DateTimeField('CREATED_TIME', auto_now_add=True)
  UPDATED_BY = models.CharField('UPDATED_BY', max_length=32)
  UPDATED_TIME = models.DateTimeField('UPDATED_TIME', auto_now=True)
  ffts_id = models.CharField('FFTS ID', unique=True, max_length=50, default='Auto-Generation')
  business_flow = models.CharField('Business Flow', max_length=38, help_text='e.g.: BU_SRC_TO_DEST_UAT')
  strategy = models.CharField('Strategy', max_length=15, choices=(('Polling', 'Polling'), ('Trigger', 'Trigger'), ('Initialization', 'Initialization')))
  config_sync = models.CharField('Config Sync?', max_length=1, default='N')
  dest_array = models.CharField('dest.array', max_length=1024, default='null')
  dest_array_help = models.CharField('dest.array.help', max_length=1024, default='sftp', choices=(('sftp', 'sftp'), ('ftps', 'ftps'), ('s3', 's3')))
  app_support_team = models.CharField('app.support.team', max_length=128, default='PLEASE-SUPPRESS-INCIDENT')
  app_support_callout = models.CharField('app.support.callout', max_length=6, default='TICKET',
                                         choices=(('BHO', 'BHO'), ('7x24', '7x24'), ('TICKET', 'TICKET')))
  app_support_team_email_id = models.CharField('app.support.team.email.id', max_length=256, default='null')
  short_retry_failure_email = models.CharField('short.retry.failure.email', max_length=256, default='null')
  long_retry_email = models.CharField('long.retry.email', max_length=256, default='null')
  source_resource = models.CharField('source.resource', max_length=512, default='null')
  source_folder = models.CharField('source.folder', max_length=256, default='null')
  project_desc = models.CharField('project.desc', max_length=1024, default='null')

  # def ffts_id(self):
  #   return 'FFTS' + str(self.id).rjust(10, '0') + '_' + self.business_flow
  #
  # ffts_id.admin_order_field = 'business_flow'
  # ffts_id.short_description = 'FFTS ID'

  def __str__(self):
    return self.ffts_id
