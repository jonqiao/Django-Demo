from django.urls import path

from . import apps
from . import views

app_name = apps.FftsConfig.name  # 重点是这一行

urlpatterns = [
  path('api/project/', views.new_project, name='new_project'),
]
