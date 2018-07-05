from django.conf.urls import url
from django.contrib import admin
from userapp import views
from artapp import views_art


urlpatterns = [
    # 声明主页面的请求
    url('^register$', views.register),

]