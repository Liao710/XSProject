import json
import os
import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from XSProject import settings
from userapp.forms import UserForm
from userapp.models import UserProfile


# Create your views here.


def regist(request):

    if request.method == 'GET':
        return render(request, 'user/regist.html')

    else: # post
        # user = UserProfile()
        # user.username = request.POST.get('username')
        # user.password = request.POST.get('password')
        # user.phone = request.POST.get('phone')
        # user.photo = request.FILES.get('photo')

        # 创建userform实例对象
        #  要求: 表单中指定的字段名必须和models模型里的字段名一致
        userForm = UserForm(request.POST)

        # 保存之前要验证密码
        if userForm.is_valid():  # 验证成功
            userForm.save()
            return redirect('/art/')

        else:
            print('验证出错了',userForm.errors)
            # form.errors.as_json() 返回的是字符串
            # 格式 {'字段名':['message':'xxx','code':'required'],
            #       '字段名2':['message':'xxx','code':'required']}
            return render(request, 'user/regist.html',
                          {'errors':json.loads(userForm.errors.as_json())})


@csrf_exempt  # 装饰函数,不验证csrf的token
def upload(request):
    # 实现图片文件上传的功能(接口)
    # 请求方法:post
    # 请求参数: photo 文件类型

    # 实现功能
    uploadFile = request.FILES.get('photo')
    print(uploadFile)

    # 配置文件保存的路径和文件名
    imgDir = os.path.join(settings.MEDIA_ROOT,'users')
    # uuid.uuid4()唯一的,有"-"间隔,后面为后缀
    imgFileName = str(uuid.uuid4()).replace('-','')+'.'+uploadFile.name.split('.')[-1]

    # 将上传文件内容写入到服务器中
    with open(os.path.join(imgDir,imgFileName),'wb') as f:
        for chunk in uploadFile.chunks():
            f.write(chunk)

    print('文件上传成功')



    # 响应的数据
    return JsonResponse({'status':'ok','path':'users/'+imgFileName})


def login(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 1.根据用户名查找用户信息
        res = UserProfile.objects.filter(username=username)
        if not res.exists():
            errors.append(username+'用户不存在')

        else:
            # 从查询结果中读取第一个记录
            user:UserProfile = res.first()
            if not user.varify_password(password):
                print(1)
                # 密码不一样
                errors.append('密码错误,请重试')

            # 登录成功,
            else:
                # 向session中写入 user 唯一标识
                request.session['user_id'] = user.id
                print(2)

                return redirect('/art/')


    # 用户登录
    return render(request, 'user/login.html', {'errors':errors})


def logout(request):
    # 清除session
    request.session.flush()

    return redirect('/art/')