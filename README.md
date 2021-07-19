# Django-Demo
Django first demo... Let's go...


## 一 新建项目
进入你期望的项目保存目录，运行下面的命令：
```shell
$ django-admin startproject mysite
```
一个新建立的项目结构大概如下：
```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```
各文件和目录解释：
- 外层的mysite/目录与Django无关，只是你项目的容器，可以任意重命名。
- manage.py：一个命令行工具，管理Django的交互脚本。
- 内层的mysite/目录是真正的项目文件包裹目录，它的名字是你引用内部文件的Python包名，例如：mysite.urls。
- mysite/__init__.py:一个定义包的空文件。
- mysite/settings.py:项目的配置文件。
- mysite/urls.py:路由文件，所有的任务都是从这里开始分配，相当于Django驱动站点的目录。
- mysite/wsgi.py:一个基于WSGI的web服务器进入点，提供底层的网络通信功能，通常不用关心。
- mysite/asgi.py：一个基于ASGI的web服务器进入点，提供异步的网络通信功能，通常不用关心。


## 二 启动开发服务器
Django提供了一个用于开发的web服务器，使你无需配置一个类似Ngnix的生产服务器，就能让站点运行起来。 这是一个由Python编写的轻量级服务器，简易但不安全，因此不要将它用于生产环境。

打开浏览器，访问http://127.0.0.1:8000/，你将看到Django的火箭欢迎界面，一切OK！

Django的开发服务器（以后简称服务器）默认运行在内部的8000端口，如果你想指定端口，请在命令中显示给出：
```shell
$ python manage.py runserver
$ python manage.py runserver 9527
$ python manage.py runserver 0.0.0.0:9527 # 这样外网就能访问这个dev server了
$ python manage.py runserver 0:9527  #0 是 0.0.0.0 的简写
```


## 三 创建应用(app)
在 Django 中，每一个应用（app）都是一个 Python 包，并且遵循着相同的约定。Django 自带一个工具，可以帮你生成应用的基础目录结构。

app应用与project项目的区别：
- 一个app实现某个具体功能，比如博客、公共档案数据库或者简单的投票系统；
- 一个project是配置文件和多个app的集合，这些app组合成整个站点；
- 一个project可以包含多个app；
- 一个app可以属于多个project！

app的存放位置可以是任何地点，但是通常都将它们放在与manage.py脚本同级的目录下，这样方便导入文件。

进入mysite项目根目录，确保与manage.py文件处于同一级，输入下述命令：
```shell
$ python manage.py startapp polls
```
系统会自动生成 polls应用的目录，其结构如下：
```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```


## 四 编写第一个视图
下面，我们编写一个视图，也就是具体的业务代码。

在polls/views.py文件中，编写代码：
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("这里是投票站点")
```
为了调用该视图，我们还需要编写urlconf，也就是路由配置。在polls目录中新建一个文件，名字为urls.py（<font color="red">不要换成别的名字</font>），在其中输入代码如下：
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
接下来，在项目的主urls.py文件中添加urlpattern条目，指向我们刚才建立的polls这个app独有的urls.py文件，这里需要导入include模块。打开mysite/urls.py文件，代码如下：
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
  path('admin/', admin.site.urls),
  path('polls/', include('polls.urls')),
]
```
include语法相当于多级路由，它把接收到的url地址去除与此项匹配的部分，将剩下的字符串传递给下一级路由urlconf进行判断。

include的背后是一种即插即用的思想。项目的根路由不关心具体app的路由策略，只管往指定的二级路由转发，实现了应用解耦。app所属的二级路由可以根据自己的需要随意编写，不会和其它的app路由发生冲突。app目录可以放置在任何位置，而不用修改路由。这是软件设计里很常见的一种模式。

建议：除了admin路由外，尽量给每个app设计自己独立的二级路由。

好了，路由设置成功后，启动服务器，然后在浏览器中访问地址http://localhost:8000/polls/


## 五 path()方法
一个路由配置模块就是一个urlpatterns列表，列表的每个元素都是一项path，每一项path都是以path()的形式存在。

path()方法可以接收4个参数，其中前2个是必须的：route和view，以及2个可选的参数：kwargs和name。

以下面的代码为例：
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

**route**

route 是一个匹配 URL 的准则（类似正则表达式）。当 Django 响应一个请求时，它会从 urlpatterns 的第一项path开始，按顺序依次匹配列表中的项，直到找到匹配的项，然后执行该条目映射的视图函数或下级路由，其后的条目将不再继续匹配。因此，url路由执行的是短路机制，path的编写顺序非常重要！

例子中对应的route就是空字符串''

需要注意的是，route不会匹配 GET 和 POST 参数或域名。例如，URLconf 在处理请求 https://www.xxx.com/myapp/时，它会尝试匹配 myapp/。处理请求 https://www.xxx.com/myapp/?page=3 时，也只会尝试匹配 myapp/。

**view**

view指的是处理当前url请求的视图函数。当Django匹配到某个路由条目时，自动将封装的HttpRequest对象作为第一个参数，被“捕获”的参数以关键字参数的形式，传递给该条目指定的视图view。

例子中对应的view就是views.index

**kwargs**

任意数量的关键字参数可以作为一个字典传递给目标视图。

本例中没有使用这个参数。

**name**

对你的URL进行命名，让你能够在Django的任意处，尤其是模板内显式地引用它。这是一个非常强大的功能，相当于给URL取了个全局变量名，不会将url匹配地址写死。


## 六 admin后台管理站点

1. 创建管理员用户

```shell
$ python manage.py createsuperuser
```

2. 启动开发服务器

  执行runserver命令启动服务器后，在浏览器访问http://127.0.0.1:8000/admin/。
  小技巧：
  在实际环境中，为了站点的安全性，我们一般不能将管理后台的url随便暴露给他人，不能用/admin/这么简单的路径。
  
  可以将根url路由文件mysite/urls.py中admin.site.urls对应的表达式，换成你想要的，比如：
  
```python
from django.contrib import admin 
from django.urls import include, path
  
urlpatterns = [
  path('admin/', admin.site.urls),
  path('polls/', include('polls.urls')),
]
```

  这样，我们必须访问http://127.0.0.1:8000/control/才能进入admin界面。

3. 进入站点

  利用刚才建立的admin账户，登陆admin，你将看到admin的界面。

4. 注册投票应用

  现在还无法看到投票应用，必须先在admin中进行注册，告诉admin站点，请将polls的模型加入站点内，接受站点的管理。
  
  打开polls/admin.py文件，加入下面的内容：
```python
from django.contrib import admin
from .models import Question

admin.site.register(Question)
```

5. 站点体验

  注册question模型后，等待服务器重启动，然后刷新admin页面就能看到Question栏目了。


6. 如果关闭debug模式后，请执行以下命令将simpleui静态文件静态文件克隆到根目录
```
python3 manage.py collectstatic
```

7. 克隆静态文件出错 请在settings.py文件中加入：
```
STATIC_ROOT = os.path.join(BASE_DIR, "static")
```