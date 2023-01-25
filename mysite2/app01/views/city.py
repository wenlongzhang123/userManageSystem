from django.shortcuts import render, redirect
from app01 import models
from django import forms
def city_list(request):
    queryset = models.City.objects.all()
    return render(request, "city_list.html", {"queryset": queryset})


class UpModalForm(forms.ModelForm):
    class Meta:
        model = models.City
        fields = "__all__"


def city_add(request):
    title = "新建城市"
    if request.method == "GET":
        form = UpModalForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})
    form = UpModalForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()  # 对于文件：自动保存; 字段 + 上传路径写入到数据库
        return redirect("/city/list/")
    return render(request, 'upload_form.html', {"form": form, "title": title})