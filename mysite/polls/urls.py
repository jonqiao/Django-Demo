from django.urls import path

from . import apps
from . import views

app_name = apps.PollsConfig.name  # 重点是这一行

urlpatterns = [
  path('fbv/', views.fbv_index, name='fbvIndex'),
  path('fbv/<int:question_id>/', views.fbv_detail, name='fbvDetail'),
  path('fbv/<int:question_id>/results/', views.fbv_results, name='fbvResults'),
  path('fbv/<int:question_id>/vote/', views.fbv_vote, name='fbvVote'),
  path('cbv/', views.IndexView.as_view(), name='cbvIndex'),
  path('cbv/<int:pk>/', views.DetailView.as_view(), name='cbvDetail'),
  path('cbv/<int:pk>/results/', views.ResultsView.as_view(), name='cbvResults'),
  path('cbv/<int:pk>/vote/', views.cbv_vote, name='cbvVote'),
]
