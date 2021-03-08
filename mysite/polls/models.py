import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
  CREATED_BY = models.CharField('created_by', max_length=32)
  CREATED_TIME = models.DateTimeField('created_ts', auto_now_add=True)
  UPDATED_BY = models.CharField('updated_by', max_length=32)
  UPDATED_TIME = models.DateTimeField('updated_ts', auto_now=True)
  question_text = models.CharField('question', max_length=200)
  pub_date = models.DateTimeField('date published')
  sync_config = models.CharField('sync_config', max_length=3, default='N')

  def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now

  was_published_recently.admin_order_field = 'pub_date'
  was_published_recently.boolean = True
  was_published_recently.short_description = 'Published recently?'

  def __str__(self):
    return self.question_text


SELECT_CHOICES = (('BMW', 'BMW'),
                  ('Mercedes Benz', 'Mercedes Benz'),
                  ('AUDI', 'AUDI'),
                  ('LEXUS', 'LEXUS'),
                  ('Apple', 'Apple'),
                  ('Grape', 'Grape'),
                  ('Orange', 'Orange'))


class Choice(models.Model):
  CREATED_BY = models.CharField('created_by', max_length=32)
  CREATED_TIME = models.DateTimeField('created_ts', auto_now_add=True)
  UPDATED_BY = models.CharField('updated_by', max_length=32)
  UPDATED_TIME = models.DateTimeField('updated_ts', auto_now=True)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField('choice', max_length=200, choices=SELECT_CHOICES, help_text='please choice one...')
  votes = models.IntegerField('choice votes', default=0)

  def __str__(self):
    return self.choice_text
