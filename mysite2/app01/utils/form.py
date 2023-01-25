from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01 import models
from app01.utils.encrypt import md5
from app01.utils.bootstrap import BootStrapModelForm

class UserForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]

    def __init__(self, *arge, **kwargs):
        super().__init__(*arge, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"placeholder": field.label}

class PrettyForm(forms.ModelForm):
    # 格式错误（办法一） ↓↓↓↓↓↓↓↓↓↓↓
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"   // 获取所有字段
        # exclude = ['level']   // 排除level所有的
    # 不是很重要↓↓↓↓↓↓↓↓↓↓↓↓
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for mobile, field in self.fields.items():
    #         field.widget.attrs = {"placeholder": field.label}
    # 格式错误（办法二） ↓↓↓↓↓↓↓↓↓↓↓
    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data["mobile"]
    #     if len(txt_mobile) != 11:
    #         raise ValidationError("格式错误")
    #     return txt_mobile
    # 手机号已存在（新建靓号中） ↓↓↓↓↓↓↓↓↓↓↓

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile

class PrettyEditForm(forms.ModelForm):
    # 格式错误（办法一） ↓↓↓↓↓↓↓↓↓↓↓
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    # 禁止编辑手机号 ↓↓↓↓↓↓↓↓↓↓↓
    # mobile = forms.CharField(disabled=True, label="手机号")

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    # 不是很重要 ↓↓↓↓↓↓↓↓↓↓↓
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for mobile, field in self.fields.items():
    #         field.widget.attrs = {"placeholder": field.label}
    # 格式错误（办法二） ↓↓↓↓↓↓↓↓↓↓↓
    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data["mobile"]
    #     if len(txt_mobile) != 11:
    #         raise ValidationError("格式错误")
    #     return txt_mobile
    # 手机号已存在（编辑靓号中） ↓↓↓↓↓↓↓↓↓↓↓
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile

class AdminForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput  # 密码不清空： widget=forms.PasswordInput（render_value=True）
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput,  # "password":forms.PasswordInput(render_value=True)
        }

    def __init__(self, *age, **kwargs):
        super().__init__(*age, **kwargs)
        for username, field in self.fields.items():
            field.widget.attrs = {"placeholder": field.label}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入")
        return confirm

class AdminEditForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]

    def __init__(self, *arge, **kwargs):
        super().__init__(*arge, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"placeholder": field.label}

class AdminResetForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput  # 密码不清空： widget=forms.PasswordInput（render_value=True）
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput,  # "password":forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        exists = models.Admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前一致！")
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入")
        return confirm

class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin"]