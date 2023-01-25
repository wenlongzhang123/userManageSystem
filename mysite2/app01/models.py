from django.db import models

# Create your models here.
class Admin(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='部门', max_length=32)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    ''' 员工表 '''
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")
    depart = models.ForeignKey(verbose_name="所属部门", to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

class PrettyNum(models.Model):
    ''' 靓号 '''
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)
    level_choices = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = (
        (0, "未占用"),
        (1, "已占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=0)

    # def __str__(self):
    #     return self.

class Order(models.Model):
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="商品名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status_choice = (
        (1, "待支付"),
        (2, "已支付")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", to_field="id", on_delete=models.CASCADE)

class Boss(models.Model):
    """ 上传文件表 """
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="图片路径", max_length=128)

class City(models.Model):
    """ 上传城市文件表 """
    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")
    img = models.FileField(verbose_name="logo", max_length=128, upload_to='city/')

