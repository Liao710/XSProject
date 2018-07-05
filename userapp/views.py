import json

from django.shortcuts import render, redirect

from userapp.forms import UserForm
from userapp.models import UserProfile
# Create your views here.
def regist(request):

    if request.method == 'GET':
        return render(request,'user/regist.html')

    else: # post
        # user = UserProfile()
        # user.username = request.POST.get('username')
        # user.password = request.POST.get('password')
        # user.phone = request.POST.get('phone')
        # user.photo = request.FILES.get('photo')

        # 创建userform实例对象
        #  要求: 表单中指定的字段名必须和models模型里的字段名一致
        userForm = UserForm(request.POST,request.FILES)

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

