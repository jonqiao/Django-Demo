from django.contrib import admin

from .models import Question, Choice


# Register your models here.
# admin.site.register(Question)
# admin.site.register(Choice)


class ChoiceInline(admin.StackedInline):
  model = Choice
  extra = 0
  readonly_fields = ('CREATED_BY', 'CREATED_TIME', 'UPDATED_BY', 'UPDATED_TIME')
  radio_fields = {'choice_text': admin.HORIZONTAL}
  fieldsets = (
    ('-- Item-Content', {
      'classes': ('wide', 'collapse'),
      'fields': (('CREATED_BY', 'CREATED_TIME', 'UPDATED_BY', 'UPDATED_TIME'), 'choice_text', 'votes')
    }),
  )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  inlines = [ChoiceInline]
  list_per_page = 50  # default 100
  list_max_show_all = 200  # default 200
  readonly_fields = ('CREATED_BY', 'CREATED_TIME', 'UPDATED_BY', 'UPDATED_TIME',)
  list_display = ('question_text', 'pub_date', 'was_published_recently', 'sync_config', 'CREATED_BY', 'CREATED_TIME', 'UPDATED_BY', 'UPDATED_TIME',)
  list_display_links = ('question_text',)
  list_filter = ['pub_date']
  date_hierarchy = 'pub_date'
  search_fields = ['question_text']
  fieldsets = [
    (None, {'fields': ['question_text']}),
    ('Set Publish Date', {'fields': ['pub_date'], 'classes': ['collapse']}),
  ]

  def save_model(self, request, obj, form, change):
    if change:
      obj.UPDATED_BY = request.user.username
      obj.sync_config = 'N'
    else:
      obj.CREATED_BY = request.user.username
      obj.UPDATED_BY = request.user.username
      obj.save()
      obj.question_text = 'FFTS-bak' + str(obj.id).rjust(10, '0') + '_' + obj.question_text
    obj.save()

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for instance in instances:
      if change:
        if not instance.CREATED_BY:
          instance.CREATED_BY = request.user.username
        instance.UPDATED_BY = request.user.username
      else:
        instance.CREATED_BY = request.user.username
        instance.UPDATED_BY = request.user.username
      instance.save()
    formset.save_m2m()


# class ChoiceAdmin(admin.ModelAdmin):
#   readonly_fields = ('CREATED_BY', 'CREATED_TIME', 'UPDATED_BY', 'UPDATED_TIME',)
#   list_display = ('question', 'choice_text', 'votes', 'CREATED_BY', 'CREATED_TIME', 'UPDATED_BY', 'UPDATED_TIME',)
#   list_display_links = ('choice_text',)
#   search_fields = ['choice_text']
#   fields = ('question', ('choice_text', 'votes'))
#
#   def save_model(self, request, obj, form, change):
#     if change:
#       obj.UPDATED_BY = request.user.username
#       obj.save()
#     else:
#       obj.CREATED_BY = request.user.username
#       obj.UPDATED_BY = request.user.username
#       obj.save()


# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice, ChoiceAdmin)
