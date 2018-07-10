from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from artapp.models import  ArtTag,Art
# Create your views here.
from userapp.models import UserProfile


def index(request):
    # 获取请求参数中的tag标签分类的id
    tag_id = request.GET.get('tag')
    page_num = request.GET.get('page')

    if not page_num:
        page_num = 1  # 从第一个开始

    # 如果tag_id不存在时,则表示为所有(即不分类型)
    if (not tag_id) or (tag_id == '0'):
        tag_id = 0
        arts = Art.objects.all()
    # 根据分类查找
    else:
        arts = Art.objects.filter(tag_id=tag_id).all()

    # 分页器,每页显示4条数据
    paginator = Paginator(arts,3)
    #  获取第 page_num 页
    # 判断当前页码是否大于最大页数
    if int(page_num) > paginator.num_pages:
        page_num = paginator.num_pages
    # 判断页码是否小于等于0
    elif int(page_num) <= 0:
        page_num = 1
    page = paginator.page(page_num)
    print(paginator.page_range)

    # 从session中读取user_id,获取当前的登录的用户信息
    user_id = request.session.get('user_id')

    user = None
    if user_id:
        user = UserProfile.objects.get(id=user_id)
        # user = user.first()

    # 返回渲染模板
    return render(request, 'art/list.html', context = {'arts':page.object_list ,
                                                     'page_range':paginator.page_range,
                                                     'page':page,
                                                     'tag_id':int(tag_id),
                                                     'tags':ArtTag.objects.all(),
                                                     'user': user})



def add_tags(request):
    # 第一次跳转,编辑
    if request.method == 'GET':
        # 新增编辑(不带tag的id),修改编辑(带tag的id) ,
        # 判断是否为修改
        id = request.GET.get('id')
        # print(id)  # 1
        # print(type(id))  # str
        tag = None
        if id :
            # 存在id,即为修改
            tag = ArtTag.objects.get(id=id)
        return render(request, 'art/edit_tags.html', {'tag':tag})

    # 第二次跳转,为表单的post提交,新增修改
    else:
        # post 请求
        # 新增 和 修改
        if request.POST.get('id'):
            tag = ArtTag.objects.get(id = request.POST.get('id'))
        else:
            tag = ArtTag()
        tag.title = request.POST.get('title')
        tag.save()  # 保存到数据库
        return redirect('/art/list_tags')  # 重定向


def delete_tag(request):
    id = request.GET.get('id')
    if id:
        result = ArtTag.objects.filter(id=id)
        # print(result)  # <QuerySet [<ArtTag: ArtTag object>]>
        # print(type(result))  # <class 'django.db.models.query.QuerySet'>
        # 判断查询集是否存在
        if result.exists():
            result.delete()
    # 重定向到列表页面
    return redirect('/art/list_tags')


def list_tags(request):
    return render(request, 'art/tags_list.html',
                  context={'tags':ArtTag.objects.all()})


