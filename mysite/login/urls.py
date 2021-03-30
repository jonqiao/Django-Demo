from django.urls import path
from . import views

from . import apps

app_name = apps.LoginConfig.name  # 重点是这一行

urlpatterns = [
  path('', views.index),
  path('index/', views.index),
]
