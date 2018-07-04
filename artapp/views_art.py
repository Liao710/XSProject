from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from artapp.models import  ArtTag,Art
# Create your views here.

#  新增文章编辑函数
def edit_art(request):
    # 正常跳转
    if request.method == 'GET':
        return render(request,'art/edit_art.html',{'tags':ArtTag.objects.all()})

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
            return render(request,'art/edit_art.html',
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
