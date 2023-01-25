import json

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt


def task_list(request):
    return render(request, "task_list.html")

@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, "data": [11, 22, 33]}
    return HttpResponse(json.dumps(data_dict))
    # return JsonResponse(data_dict)