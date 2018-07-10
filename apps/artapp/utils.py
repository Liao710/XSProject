import time

from django.core.cache import cache
from django.http import HttpRequest,HttpResponse
from redis import Redis

from artapp.models import Art

rds = Redis(host='127.0.0.1',db=2)

# 声明一个view处理函数的装饰器
def cache_page(timeout):
    def wrapper_view(view_func):
        def wrapper(request:HttpRequest,*args,**kwargs):
            print('---处理%s 请求,view---' % request.get_full_path())
            url = request.get_full_path()
            print(url)
            # 根据url请求路径从缓存中读取内容
            page = cache.get(url)
            if not page:
                time.sleep(2)
                response:HttpResponse = view_func(request)
                # 将响应的内容存放到缓存中
                cache.set(url,response.content,timeout)
                return response
            else:
                return HttpResponse(page)
        return wrapper
    return wrapper_view

# 获取排行榜文章
def top5Art():
    # 得到数据格式
    # [(<Art (1)> , 300),
    #   (<Art (3)> , 200),
    # (< Art (4) >, 180),
    # (< Art (8) >, 130),
    # (< Art (10) >, 40),
    # ]
    # 从redis中读取前5的排行,返回列表,列表里面是元组
    rank_art = rds.zrevrange('Rank-Art',0,4,withscores=True)
    # id.decode():id为字节类型,需要解码
    rank_ids = [ id.decode() for id,_ in rank_art]

    # 根据 rank_ids 查询所有数据并返回字典,key为id,value为Art类对象
    arts = Art.objects.in_bulk(rank_ids)

    top_arts = [(arts.get(int(id.decode())),score) for id,score in rank_art ]

    return top_arts


