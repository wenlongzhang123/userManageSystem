from django.shortcuts import render
from django.http import JsonResponse
def chart_list(request):
    return render(request, "chart_list.html")

def chart_bar(request):
    """ 构造柱状图的数据 """
    legend = ["销量", "变量"]
    series_list = [
        {
            "name": '销量',
            "type": 'bar',
            "data": [20, 40, 50, 30, 30, 50]
        },
        {
            "name": '变量',
            "type": 'bar',
            "data": [50, 70, 20, 35, 80, 50]
        }
    ]
    x_axis = ['一月', '二月', '三月', '四月', '五月', '六月']
    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series": series_list,
            "x_axis": x_axis,
        }
    }
    return JsonResponse(result)

def chart_pie(request):
    """ 构造饼图的数据 """
    db_data_list = [
        {"value": 2048, "name": 'IT部门'},
        {"value": 1735, "name": '研发部'},
        {"value": 580, "name": '新媒体'},
    ]
    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)