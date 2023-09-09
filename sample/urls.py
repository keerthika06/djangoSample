"""
URL configuration for sample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from article.views import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static





urlpatterns = [
    path('',home, name="home"),
    path('article/',articles,name="article"),
    path('login/',login_page, name ="login_page"),
    path('add-user/',register_page,name="register_page"),
    path('admin/', admin.site.urls),
    path('add-article/',add_article,name ="add_article"),
    path('show-article/',showArticle,name ="showArticle"),
    path('update-article/<id>/',update_article,name ="update_article"),
    path('delete-article/<id>/',delete_article,name="delete_article"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)



urlpatterns += staticfiles_urlpatterns()