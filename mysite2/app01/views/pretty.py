from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import PrettyForm, PrettyEditForm

def pretty_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile=18888888888, price=200, level=2, status=0)
    # page = int(request.GET.get("page",1))
    # page_size = 10
    # start = (page - 1) * page_size
    # end = page *page_size
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("level")
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    # total_count = models.PrettyNum.objects.filter(**data_dict).o.count()
    # total_page_count, div = divmod(total_count, page_size)

    # if div:
    #     total_page_count += 1
    # page_str_list = []
    # for i in range(1,total_page_count + 1):
    #     ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
    #     page_str_list.append(ele)
    # page_string = mark_safe("".join(page_str_list))
    return render(request, "pretty_list.html", context)

def pretty_add(request):
    if request.method == "GET":
        form = PrettyForm()
        return render(request, "pretty_add.html", {"form": form})
    form = PrettyForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_add.html", {"form": form})

def pretty_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})
    form = PrettyEditForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"form": form})

def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")