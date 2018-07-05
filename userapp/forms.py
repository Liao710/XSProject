from django import forms
from django.core.exceptions import ValidationError

from userapp.models import UserProfile


class UserForm(forms.ModelForm):
    # 新增一个字段(password2)

    password2 = forms.CharField(max_length=50,label='确认密码')

    class Meta:
        # 当前form表单对应的模型类
        # 作用:读取数据
        model = UserProfile
        # 显示或验证的字段
        #如果验证所有字段,则"__all__"
        # 如果知道字段,则['字段名1','字段名3',...]
        fields = '__all__'

        # 当前Form如果生成字段标签时,显示的label的名称
        # 在网页中: {{ form.as_p() }}
        labels = {
            'username':'用户名',
            'password':'密码'
        }

        # widgets

        # 验证错误消息
        error_messages = {
            'username': {'required': '用户名不能为空'},
            'password': {'required': '密码不能为空'},
            'phone': {'required': '手机号不能为空'},
            'photo': {'required': '头像不能为空'},
            'password2':{'required':'确认密码不能为空'}

        }

    # 主要验证数据是否为空
    def is_valid(self):
        # 调用父类的form表单的验证方法
        # cleaned_data 是字典类型,只有执行了form的is_valid函数才会生成的'干净'的数据
        return super().is_valid()


    # 验证两次密码是否相同:(如何从请求中获取models中不存在的属性字段值)
    # 清除password2数据 的空格
    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 !=  password2:
            # 若抛出异常时,则会由form的errors收集
            raise ValidationError('两次密码输入不一致')

        return self.cleaned_data.get('password')


    # 通过正则验证手机号
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')


        return phone











