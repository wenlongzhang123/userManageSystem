import os
from django.shortcuts import render, HttpResponse
from django import forms
from app01 import models

def upload_list(request):
    if request.method == "GET":
        return render(request, "upload_list.html")

    # print(request.GET)
    # print(request.FILES)

    file_object = request.FILES.get("avatar")
    # print(file_object.name)  => m.png
    f = open(file_object.name, mode='wb')  # mode 打开方式读写

    for chunk in file_object.chunks():  # 一点一点的去读
        f.write(chunk)
    f.close()

    return HttpResponse("...")

class UpForm(forms.Form):
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")

def upload_form(request):
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, "upload_form.html", {"form": form, "title": title})
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # {'name': '是是是', 'age': 20, 'img': < InMemoryUploadedFile: m.png(image / png) >}
        # print(form.cleaned_data) => 获取数据 + 文件对象
        # 1.读取文件内容，写入到文件夹中并获取文件的路径。
        image_object = form.cleaned_data.get("img")
        # 方法一
        # db_file_path = os.path.join("static", "img", image_object.name)  # 使用os拼接要存入数据库的路径。
        # file_path = os.path.join("app01", db_file_path)  # 使用os拼接要存入pycharm的路径。
        # 方法二
        media_path = os.path.join("media", image_object.name)
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        # 2.将图片文件路径写入到数据库。
        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            img=media_path,
        )
        return render(request, "upload_form.html", {"form": form, "title": title})
    return render(request, "upload_form.html", {"form": form, "title": title})

class UpModalForm(forms.ModelForm):
    class Meta:
        model = models.City
        fields = "__all__"

def upload_modal_form(request):
    """ 上传文件和数据（ModalForm）"""
    title = "ModalForm上传文件"
    if request.method == "GET":
        form = UpModalForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})
    form = UpModalForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()  # 对于文件：自动保存; 字段 + 上传路径写入到数据库
        return HttpResponse("成功")
    return render(request, 'upload_form.html', {"form": form, "title": title})
