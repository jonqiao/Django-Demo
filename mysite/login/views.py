from django.shortcuts import render
from login import models

# Create your views here.
userList = []


def index(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username, password)
    # 将数据保存到数据库
    models.UserInfo.objects.create(username=username, password=password)

  # 从数据库中读取所有数据，注意缩进
  userList = models.UserInfo.objects.all()
  # return HttpResponse('Hello World!')
  return render(request, 'login/index.html', {'data': userList})
