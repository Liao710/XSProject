from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    username = models.CharField(max_length=50,verbose_name='用户名')
    #  diango的密码生成器 ,  make_password
    password = models.CharField(max_length=100,verbose_name='密码')
    phone = models.CharField(max_length=13,verbose_name='联系电话',null=True)
    # upload_to 指定的路径是相对于settings.py中MEDIA_ROOT设置的路径
    photo = models.ImageField(upload_to='users',verbose_name='头像',null=True)
    # 注册时间
    regist_time = models.DateTimeField(auto_now_add=True,verbose_name='注册时间')
    # 最后登陆时间
    login_time = models.DateTimeField(auto_now=True,verbose_name='最近登录时间')


    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户信息'

    def save(self):
        # hash密码生成器
        # 判断是否已加密,已加密则不再加密,未加密则加密
        if self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save()

    # 登录时,验证密码是否正确
    # 先核对用户是否存在,不存在则跳转,存在则验证密码
    def varify_password(self,password):

        # 验证密码是否正确,
        # password为明文,后面self.password为密文
        return check_password(password,self.password)


















