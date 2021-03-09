import urllib
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from shutil import copy, copy2
from xml.etree.ElementTree import ElementTree

from django.conf import settings
from django.contrib import admin, messages
from django.core import serializers
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import ngettext
from simpleui.admin import AjaxAdmin

from .models import Project

admin.site.site_title = 'TIS MIDDLEWARE'
admin.site.site_header = 'TIS Middleware'
admin.site.index_title = 'Middleware Index'
# disable delete site-wide action
admin.site.disable_action('delete_selected')


# Register your models here.
def find_xml_nodes(configfile, tag):
  tree = ElementTree()
  tree.parse(configfile)
  nodes = tree.findall(tag)
  return tree, nodes


def sync_from_xml(configfile, obj):
  tree, nodes = find_xml_nodes(configfile, "project_variable")
  for node in nodes:
    name = node.findtext('project_name', 'NOT.FOUND').replace('.', '_')
    value = node.findtext('project_value', 'null')
    setattr(obj, name, value)
    if name == 'source_resource':
      if value == 'null':
        obj.strategy = 'Trigger'
      else:
        obj.strategy = 'Polling'


def sync_to_xml(configfile, obj):
  tree, nodes = find_xml_nodes(configfile, "project_variable")
  for node in nodes:
    name = node.findtext('project_name', 'NOT.FOUND').replace('.', '_')
    node.find('project_value').text = getattr(obj, name, 'null')
  tree.write(configfile, encoding="utf-8", xml_declaration=True)


@admin.register(Project)
class ProjectAdmin(AjaxAdmin):
  save_on_top = True
  # save_as = True
  list_per_page = 100  # default 100
  list_max_show_all = 200  # default 200
  readonly_fields = ('config_sync', "CREATED_BY", 'CREATED_TIME', 'UPDATED_BY', 'UPDATED_TIME',)
  list_display = ('ffts_id', 'strategy', 'config_sync', "CREATED_BY", 'CREATED_TIME', 'UPDATED_BY', 'UPDATED_TIME',)
  list_display_links = ('ffts_id',)
  list_filter = ['strategy', 'config_sync', "CREATED_BY"]
  date_hierarchy = 'CREATED_TIME'
  search_fields = ['ffts_id']
  radio_fields = {"strategy": admin.HORIZONTAL}
  fieldsets = [
    (None, {'fields': ['ffts_id', 'business_flow', 'strategy']}),
    ('Configuration',
     {'classes': ['collapse'],
      'fields': [('dest_array', 'dest_array_help'), 'app_support_team', 'app_support_callout',
                 'app_support_team_email_id', 'short_retry_failure_email', 'long_retry_email',
                 'source_resource', 'source_folder', 'project_desc']
      }
     ),
  ]
  actions = ['sync_to_configfile', 'sync_from_configfile', 'sync_init_configfile', 'promote_project']

  # disable delete action for this model only
  # def get_actions(self, request):
  #   actions = super().get_actions(request)
  #   if 'delete_selected' in actions:
  #     del actions['delete_selected']
  #   return actions

  def get_readonly_fields(self, request, obj=None):
    if obj:
      return ['ffts_id', 'business_flow', self.readonly_fields]
    else:
      return self.readonly_fields

  def save_model(self, request, obj, form, change):
    if change:
      obj.UPDATED_BY = request.user.username
      obj.config_sync = 'N'
    else:
      obj.CREATED_BY = request.user.username
      obj.UPDATED_BY = request.user.username
      obj.save()
    if not obj.ffts_id or obj.ffts_id == 'Auto-Generation':
      obj.ffts_id = 'FFTS' + str(obj.id).rjust(10, '0') + '_' + obj.business_flow
    obj.save()

  def delete_model(self, request, obj):
    # if configfile exist, rename it with datetime suffix
    dt = datetime.now().strftime('%Y%m%d%H%M%S')
    configfile = settings.CONFIGDIR + obj.ffts_id + '.xml'
    configbak = configfile + '.' + dt + '.del'
    if Path(configfile).is_file():
      # os.rename(configfile, configbak)
      Path(configfile).rename(configbak)
    obj.delete()

  # customized action
  def sync_init_configfile(self, request, queryset):
    """
    1: get all the configfile in configdir
    2: create obj with configfile if related project is not existed in db
    3: update model config_sync = 'Y' and strategy = 'Trigger' or 'Polling'
    """
    if len(queryset) == 1 and 'SYNC_INIT_FROM_CONFIGURATION' == queryset[0].ffts_id:
      count = 0
      for configfile in Path(settings.CONFIGDIR).glob('FFTS*.xml'):
        ffts_id = configfile.name.split('.')[0]
        obj = Project.objects.filter(ffts_id=ffts_id)
        if not obj:
          obj = Project()
          obj.ffts_id = ffts_id
          obj.business_flow = ffts_id.split('_', 1)[1]
          sync_from_xml(configfile, obj)
          obj.config_sync = 'Y'
          obj.CREATED_BY = request.user.username
          obj.UPDATED_BY = request.user.username
          obj.save()
          count = count + 1
      queryset[0].config_sync = 'Y'
      queryset[0].save()
      self.message_user(request,
                        ngettext('%d project synchronized initialization successfully!',
                                 '%d projects synchronized initialization successfully!', count) % count,
                        messages.SUCCESS)
    else:
      self.message_user(request, 'ONLY SYNC_INIT_FROM_CONFIGURATION CAN BE SELECTED!', messages.WARNING)

  sync_init_configfile.type = 'danger'
  sync_init_configfile.icon = 'el-icon-setting'
  sync_init_configfile.confirm = 'ARE YOU SURE TO SYNCHRONIZE INITIALIZATION???'

  def sync_from_configfile(self, request, queryset):
    """
    1. if configfile has the latest values, read values from configfile
    2. update obj with new values from configfile
    3. update model config_sync = 'Y' and strategy = 'Trigger' or 'Polling'
    """
    count = 0
    for obj in queryset:
      if 'SYNC_INIT_FROM_CONFIGURATION' == obj.ffts_id:
        self.message_user(request, 'SYNC_INIT_FROM_CONFIGURATION IGNORED!', messages.WARNING)
      else:
        configfile = settings.CONFIGDIR + obj.ffts_id + '.xml'
        if Path(configfile).is_file():
          sync_from_xml(configfile, obj)
          obj.config_sync = 'Y'
          obj.UPDATED_BY = request.user.username
          obj.save()
          count = count + 1
        else:
          self.message_user(request, obj.ffts_id + ' synchronized failed due to missing configfile!', messages.WARNING)
    self.message_user(request,
                      ngettext('%d project synchronized from configfile successfully!',
                               '%d projects synchronized from configfile successfully!', count) % count,
                      messages.SUCCESS)

  sync_from_configfile.type = 'info'
  sync_from_configfile.icon = 'el-icon-receiving'
  sync_from_configfile.confirm = 'ARE YOU SURE TO SYNCHRONIZE FROM CONFIGFILE???'

  def sync_to_configfile(self, request, queryset):
    """
    1: if configfile exist, backup it with datetime suffix
       else create it by copying from config-template
    2: update configfile with ojb new values using ElementTree
    3: update model config_sync = 'Y'
    notes: queryset.update(config_sync='Y')  # queryset自带的update()方法，能批量操作
    """
    count = 0
    for obj in queryset:
      if 'SYNC_INIT_FROM_CONFIGURATION' == obj.ffts_id:
        self.message_user(request, 'SYNC_INIT_FROM_CONFIGURATION IGNORED!', messages.WARNING)
      else:
        dt = datetime.now().strftime('%Y%m%d%H%M%S')
        configfile = settings.CONFIGDIR + obj.ffts_id + '.xml'
        configbak = configfile + '.' + dt + '.bak'
        if Path(configfile).is_file():
          copy2(configfile, configbak)
        else:
          copy(settings.CONFIGTPL, configfile)
        sync_to_xml(configfile, obj)
        obj.config_sync = 'Y'
        obj.save()
        count = count + 1
    self.message_user(request,
                      ngettext('%d project synchronized to configfile successfully!',
                               '%d projects synchronized to configfile successfully!', count) % count,
                      messages.SUCCESS)

  sync_to_configfile.type = 'success'
  sync_to_configfile.icon = 'el-icon-magic-stick'
  sync_to_configfile.confirm = 'ARE YOU SURE TO SYNCHRONIZE TO CONFIGFILE???'

  # def promote_project(self, request, queryset):
  #   count = 0
  #   for obj in queryset:
  #     if 'SYNC_INIT_FROM_CONFIGURATION' == obj.ffts_id:
  #       self.message_user(request, 'SYNC_INIT_FROM_CONFIGURATION IGNORED!', messages.WARNING)
  #     else:
  #       # POST /ffts/api/project/
  #       obj.ffts_id = obj.ffts_id[:obj.ffts_id.rfind('_') + 1] + 'PRD'
  #       obj.business_flow = obj.ffts_id.split('_', 1)[1]
  #       obj.config_sync = 'N'
  #       obj.CREATED_BY = request.user.username
  #       obj.CREATED_TIME = timezone.now()
  #       obj.UPDATED_BY = request.user.username
  #       obj.UPDATED_TIME = timezone.now()
  #       obj.id = None
  #       data = serializers.serialize('json', [obj]).encode()
  #       headers = {"Content-Type": "application/json"}
  #       remote_req = urllib.request.Request("http://127.0.0.1:8000/ffts/api/project/", data=data, headers=headers)
  #       remote_res = urllib.request.urlopen(remote_req)
  #       print(remote_res.read().decode("utf-8"))
  #       count = count + 1
  #   self.message_user(request,
  #                     ngettext('%d project promoted successfully!',
  #                              '%d projects promoted successfully!', count) % count,
  #                     messages.SUCCESS)
  # promote_project.type = 'warning'
  # promote_project.icon = 'el-icon-s-promotion'
  # promote_project.confirm = 'ARE YOU SURE TO PROMOTE TO PROD???'

  def promote_project(self, request, queryset):
    post = request.POST
    if not post.get('_selected'):
      return JsonResponse(data={
        'status': 'error',
        'msg': 'Please select at least one option!'
      })
    else:
      # 这里获取到数据后，可以做些业务处理
      promotion_env = post.get('promote_env')
      if promotion_env == 'PRD':
        remote_link = settings.REMOTE_LINK_PRD
      else:
        remote_link = settings.REMOTE_LINK_NONPRD
      count = 0
      for obj in queryset:
        if 'SYNC_INIT_FROM_CONFIGURATION' == obj.ffts_id:
          self.message_user(request, 'SYNC_INIT_FROM_CONFIGURATION IGNORED!', messages.WARNING)
        else:
          obj.ffts_id = obj.ffts_id[:obj.ffts_id.rfind('_') + 1] + promotion_env
          obj.business_flow = obj.ffts_id.split('_', 1)[1]
          obj.config_sync = 'N'
          obj.CREATED_BY = request.user.username
          obj.CREATED_TIME = timezone.now()
          obj.UPDATED_BY = request.user.username
          obj.UPDATED_TIME = timezone.now()
          obj.id = None
          data = serializers.serialize('json', [obj]).encode()
          headers = {"Content-Type": "application/json"}
          remote_req = urllib.request.Request(remote_link, data=data, headers=headers)
          remote_res = urllib.request.urlopen(remote_req)
          # print(remote_res.read().decode("utf-8"))
          count = count + 1
      return JsonResponse(data={
        'status': 'success',
        'msg': ngettext('%d project promoted successfully!',
                        '%d projects promoted successfully!', count) % count
      })

  # promote_project.short_description = "Promote project"
  promote_project.type = 'warning'
  promote_project.icon = 'el-icon-s-promotion'
  promote_project.layer = {
    'title': 'PROMOTE ENV SELECTION',
    'tips': 'Please select env you want to do the promotion...',
    'confirm_button': 'SUBMIT',
    'cancel_button': 'CANCEL',
    'params': [{
      'type': 'select',
      'key': 'promote_env',
      'label': 'ENV',
      'width': '200px',
      'size': 'small',
      'value': 'PRD',
      'options': [{
        'key': 'PRD',
        'label': 'PRD'
      }, {
        'key': 'EBF',
        'label': 'EBF'
      }, {
        'key': 'UAT',
        'label': 'UAT'
      }, {
        'key': 'SIT',
        'label': 'SIT'
      }, {
        'key': 'DEV',
        'label': 'DEV'
      }]
    }]
  }
