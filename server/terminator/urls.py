"""terminator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from skynet import views

urlpatterns = [
    url(r'^$', views.view_main),
    url(r'^t800/', include(admin.site.urls)),
    url(r'^test/', views.test_page),
    url(r'^q/domain/', views.view_domain),
    url(r'^q/page/', views.view_full_request),
    url(r'^api/put$', views.put),
    url(r'^api/get$', views.get),
    url(r'^about/', views.about_page),
    url(r'^demo/$', views.demo_page),
    url(r'^demo/get$', views.api_get_page),
    url(r'^demo/put$', views.api_put_page),
]
