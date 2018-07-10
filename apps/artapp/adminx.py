import xadmin
from xadmin import views
from artapp.models import Art,ArtTag

# 基础设置
class BaseSetting():
    # 启用主题样式选择
    enable_themes = True
    # 切换菜单
    use_bootswatch = True

# 全局设置
class GlobalSetting():
    # 配置站点标题
    site_title = '美文管理后台'
    # 配置站点的底部版权信息和友情链接
    site_footer = '千峰教育<br/>版权所有深圳Python1802'
    # 菜单样式
    menu_style ="accordion"
    # 配置全局检索类型
    global_search_models = (ArtTag,Art)

    # 配置全局模型显示的图标
    global_models_icon = {
        ArtTag:"glyphicon glyphicon-th",
        Art: "glyphicon glyphicon-list-alt"
    }

# 设置页面显示列表
class ArtTagAdmin():
    list_display = ('title',)
    search_fields = ('title',)

class ArtAdmin():
    list_display = ('title','summary','author','img','publish_time','tag')
    search_fields = ('title','author')

    # 配置文章每页显示3个
    list_per_page = 3

    # 设置字段的样式
    style_fields = {'summary':'ueditor'}

# 注册基础视图,主题风格,全局设置
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)

# 向xadmin后台注册模型类
xadmin.site.register(ArtTag,ArtTagAdmin)
xadmin.site.register(Art,ArtAdmin)









