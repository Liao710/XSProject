from django.conf.urls import url
from artapp.views import *
from artapp import views_art

urlpatterns = [
    # 声明主页面的请求
    url('^$', index),
    url(r'^tags$',add_tags),
    url(r'^delete_tag$',delete_tag),
    url(r'^list_tags$',list_tags),
    url(r'^edit_art$', views_art.edit_art),  #  编辑文字
    url(r'^search', views_art.search),  # 搜索文章
    url(r'^show', views_art.show),  # 显示文章
    url(r'^sendMsg',views_art.sendMsg)

]