from django.shortcuts import render, redirect, HttpResponse
from django import forms
from app01 import models
from app01.utils.encrypt import md5
from app01.utils.code import check_code
from io import BytesIO

class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,  # 不能为空，必填
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)


def login(request):
    """ 登录"""

    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # .pop()从cleaned_data中，把code拿出来，不是获取（也就是拿出来后，cleaned_data里就没有code了）
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', '')
        if code.upper() != user_input_code.upper():  # .upper()小写字母换成大写字母
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form})
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")  # 错误显示在密码下面
            return render(request, "login.html", {"form": form})
        request.session["info"] = {"id": admin_object.id, "username": admin_object.username}
        request.session.set_expiry(60 * 60 * 24 * 7)  # 保存七天
        return redirect("/admin/list/")

    return render(request, 'login.html', {"form": form})

def image_code(request):
    """ 生成图片验证码"""

    img, code_string = check_code()
    # 写入到自己的session中（以便于后续获取验证码在进行校验）
    request.session['image_code'] = code_string
    # 给session设置一个60秒超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def logout(request):
    """ 注销"""

    request.session.clear()

    return redirect("/login/")


