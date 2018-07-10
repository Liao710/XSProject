from django.db import models

# Create your models here.

# 小说或文章小说类型
class ArtTag(models.Model):
    title = models.CharField(max_length=20,verbose_name="作品类别",unique=True,db_index=True)
    add_time = models.DateTimeField(verbose_name="添加的时间",auto_now_add=True)
    modify_time =models.TimeField(verbose_name="最后修改时间",auto_now=True)

    class Meta:
        verbose_name = '标签分类'
        verbose_name_plural = verbose_name

    # python3 的写法,2.7为unicode
    def __str__(self):
        return self.title

from DjangoUeditor.models import UEditorField
# 文章
class Art(models.Model):
    title = models.CharField(max_length=50,unique=True,verbose_name='文章名')
    # 作者(模型,建立多对一的关联关系)
    author = models.CharField(max_length=50,blank=True,verbose_name='作者')
    # summary = models.TextField(verbose_name='简介')
    summary = UEditorField(verbose_name='概述',default='',blank=True,
                           width=800,height=600,# 显示编辑页面的宽高
                           toolbars='full', # 工具栏按钮
                           imagePath='/ueditor/images',# 上传图片路径(正文中)
                           filePath='/ueditor/files',# 上传文件的路径
                           )
    # img_url = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images/',verbose_name='文章图片',
                            blank=True,null=True)
    counter = models.IntegerField(default=0,verbose_name='阅读次数')
    publish_time = models.DateTimeField(auto_now_add=True,verbose_name='发布时间') # 当前发布时间

    # 文章类型,一端
    tag = models.ForeignKey(ArtTag,on_delete=models.SET_NULL,null=True,verbose_name='分类')



    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name





# 文章小节的模型类
