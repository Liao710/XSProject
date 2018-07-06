from django.conf.urls import url
from django.contrib import admin
from userapp import views
from artapp import views_art


urlpatterns = [
    # 声明主页面的请求
    # 注册
    url('^regist$', views.regist),
    # 登录
    url('^login$', views.login),
    # 图片上传请求
    url('^upload$', views.upload),
    # 用户登出
    url('^logout$', views.logout),

]