"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '7%-89@%b&e2z-!58$_aphn*y8oh46qfakoop=ubo@#i*dt^*ev'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '7%-89@%b&e2z-!58$_aphn*y8oh46qfakoop=ubo@#i*dt^*ev')

# SECURITY WARNING: don't run with debug turned on in production!
# 默认情况下，DEBUG的值为True，但如果DJANGO_DEBUG环境变量的值，设置为空字符串，则为False，例如，DJANGO_DEBUG=''。
DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))
# DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
# 要将应用添加到项目中,需要在INSTALLED_APPS设置中增加指向该应用的配置文件的链接.
# 配置的点式路径为polls.apps.PollsConfig,但在多数情况下,我们简写成‘polls’就可以了.

INSTALLED_APPS = [
  'simpleui',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'polls.apps.PollsConfig',
  'login',
  'FFTS',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  },
  'MySQL': {
    'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
    'HOST': '192.168.1.121',  # mysql服务所在的主机ip
    'PORT': '3306',  # mysql服务端口
    'NAME': 'mysite',  # 数据库名，先前创建的
    'USER': 'root',  # 用户名，可以自己创建用户
    'PASSWORD': 'root',  # 密码
  }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'  # 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
  BASE_DIR / 'static_common',
]

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = BASE_DIR / 'static_root'

# simpleui configuration
SIMPLEUI_STATIC_OFFLINE = True  # 离线模式
SIMPLEUI_ANALYSIS = False
SIMPLEUI_HOME_PAGE = ''
SIMPLEUI_HOME_TITLE = 'HOME'
SIMPLEUI_HOME_ICON = 'fab fa-fort-awesome'
SIMPLEUI_INDEX = 'https://www.google.com'
SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_HOME_ACTION = True
SIMPLEUI_LOADING = True

# SIMPLEUI_CONFIG = {
#   'system_keep': True,  # 关闭系统菜单
#   'dynamic': False,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
#   'menu_display': ['Authentication and Authorization', 'FFTS'],
#   'menus': [{
#     'app': 'FFTS',
#     'name': 'FFTS',
#     'icon': 'fas fa-bicycle',
#     'models': [{
#       'name': 'Project',
#       'icon': 'far fa-surprise',
#       'url': '/admin/FFTS/project/'
#     }]
#   }]
# }

# Application customer properties
CONFIGDIR = 'D://WORKSPACE//PSN-WORKSPACE//Django-Demo//configuration//'
CONFIGTPL = 'D://WORKSPACE//PSN-WORKSPACE//Django-Demo//configuration//template.xml'
REMOTE_LINK_PRD = 'http://127.0.0.1:8000/ffts/api/project/'
REMOTE_LINK_NONPRD = 'http://127.0.0.1:8000/ffts/api/project/'
