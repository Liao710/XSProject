import logging
import time

from django.core.cache import cache
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
# from django.views.decorators.cache import cache_page
from XSProject.settings import logger
from artapp import tasks
from artapp.utils import cache_page, rds, top5Art
from artapp.models import  ArtTag,Art
# Create your views here.



#  新增文章编辑函数
def edit_art(request):
    # 正常跳转
    if request.method == 'GET':
        return render(request, 'art/edit_art.html', {'tags':ArtTag.objects.all()})

    # 表单提交(post请求)
    else:
        art = Art()
        #  .strip() 去除两边空格
        title = request.POST.get('title').strip()
        summary = request.POST.get('summary').strip()
        author = request.POST.get('author').strip()
        tag_id = request.POST.get('tag').strip()
        # 获取上传文件
        img = request.FILES.get('img')
        # 内存中
        img:InMemoryUploadedFile = request.FILES.get('img')
        # 验证数据
        errors = {}
        if not title: # title 为空
            errors['title'] = '标题不能为空'
        elif len(title) > 20:
            errors['title'] = '长度不能超出20字符'

        if not author: # title 为空
            errors['author'] = '作者不能为空'
        elif len(author) > 20:
            errors['author'] = '作者名字不能超过20字符'

        # 判断验证是否存在错误
        if len(errors) > 0:
            return render(request, 'art/edit_art.html',
                          {'tags':ArtTag.objects.all(),
                           'errors':errors})

        #   保存数据
        art.title = title
        art.summary = summary
        art.author = author
        art.tag_id = tag_id
        art.img = img
        art.save()
        return redirect('/art')


def search(request):
    # 按照书名或者作者名搜索
    skey = request.POST.get('searchKey')
    arts = Art.objects.filter(Q(title__contains=skey)|Q(author__contains=skey))

    # 分页和页面布局

    return render(request, 'art/list_search.html', {'arts':arts})

# 将页面缓存到redis中
@cache_page(5)
def show(request):

    id  = request.GET.get('id') # 请求参数中的数值都是字符串


    # 设置日至等级:CRITICAL表示严重警告
    # logging.getLogger().setLevel(logging.INFO)
    # # asctime日期和时间,filename:执行日志记录调用的源文件的文件名称
    # #  funcName:执行日志记录调用的函数名称
    # formatter = '%(asctime)s:%(filename)s/%(funcName)s-%(lineno)s-->%(message)s'
    # # 配置日志的信息,filename指定要输出的文件名
    # logging.basicConfig(format=formatter,datefmt="%Y-%m-%d %H:%M:%S",
    #                     filename = 'art.log',filemode='a')


    logger.warning('---当前日志要被缓存5秒')
    # 查询文章信息
    art = Art.objects.filter(id=id).first()

    # # 先从缓存中读取(key设计:art-1)
    # page = cache.get('Art-%s' %id)
    # # 判断缓存中是否存在
    # if not page:
    #     print(1)
    #     # 加载模板文件,并渲染成html文本
    #     page = loader.render_to_string('art/art_info.html',{'art':art})
    #
    #     # 将加载完成后的页面存入到cache中
    #     cache.set('Art-%s' %id,page,10)
    # return HttpResponse(page)

    # 修改文章的点击次数,数据库中改了
    art.counter +=1
    art.save()

    # 将数据存到redis中(非cache)
    # 每次阅读都累加
    rds.zincrby('Rank-Art',id)


    return render(request, 'art/art_info.html',
                  {'art':art,
                   'top_arts':top5Art() })

def sendMsg(request):

    # 从get请求中读取必要的参数
    to = request.GET.get('to')
    msg = request.GET.get('msg')

    # 调用发送邮件任务
    # delay是task的异步任务调用的函数
    tasks.sendMail.delay(to,msg)

    return JsonResponse({'status':'ok',
                         'msg':'任务已安排'})
