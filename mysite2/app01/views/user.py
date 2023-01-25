from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import UserForm

def user_list(request):
    queryset = models.UserInfo.objects.all()
    '''
    用python的语法获取数据
    for obj in queryset:
        print(obj.create_time.strftime("%Y-%m-%d"),obj.get_gender_display(),obj.depart.title)

    '''
    return render(request, "user_list.html", {"queryset": queryset})


def user_add(request):
    if request.method == "GET":
        context = {
            "gender_choices": models.UserInfo.gender_choices,
            "queryset": models.Department.objects.all()
        }
        return render(request, "user_add.html", context)
    id = request.POST.get("id")
    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    create_time = request.POST.get("create_time")
    gender = request.POST.get("gender")
    depart = request.POST.get("depart")
    models.UserInfo.objects.create(id=id, name=name, password=password,
                                   age=age, account=account, create_time=create_time,
                                   gender=gender, depart_id=depart)
    return redirect("/user/list/")


def user_form(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, "user_form.html", {"form": form})
    form = UserForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list")

    return render(request, "user_form.html", {"form": form})


def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})
    form = UserForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")