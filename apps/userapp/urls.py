from django.conf.urls import url
from userapp import views

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