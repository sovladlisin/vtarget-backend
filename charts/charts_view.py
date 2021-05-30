from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
import json
from .models import Chart, Cabinet


@csrf_exempt
def getCharts(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        cabinet_id = data.get('cabinet_id', None)
        cabinet = Cabinet.objects.get(pk=cabinet_id)
        charts = Chart.objects.all().filter(cabinet=cabinet)
        result = []
        for chart in charts:
            temp = model_to_dict(chart)
            temp['entities'] = json.loads(temp['entities'])
            result.append(temp)
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def createChart(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        cabinet = Cabinet.objects.get(pk=data['cabinet'])

        new_chart = Chart(
            cabinet=cabinet,

            is_public=data['is_public'],
            chart_type=data['chart_type'],
            key=data['key'],
            title=data['title'],

            x=data['x'],
            y=data['y'],
            w=data['w'],
            h=data['h'],

            x_p=data['x_p'],
            y_p=data['y_p'],
            w_p=data['w_p'],
            h_p=data['h_p'],

            kpi=data['kpi'],
            unified=data['unified'],
            unified_color=data['unified_color'],
            kpi_color=data['kpi_color'],
            smooth=data['smooth'],
            pie_type=data['pie_type'],
            is_client=data['is_client'],
            start_date=data['start_date'],
            end_date=data['end_date'],

            meta=data['meta'],
            entities=json.dumps(data['entities'])
        )
        new_chart.save()
        temp = model_to_dict(new_chart)
        temp['entities'] = json.loads(temp['entities'])

        return JsonResponse(temp, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def deleteChart(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        chart = Chart.objects.get(pk=data['id'])
        chart.delete()
        return HttpResponse('Success')
    return HttpResponse('Wrong request')


@csrf_exempt
def updateChart(request):
    if request.method == 'POST':
        
        data = json.loads(request.body.decode('utf-8'))
        
        chart = Chart.objects.get(pk=data['id'])
        chart.is_public = data['is_public']
        chart.chart_type = data['chart_type']
        chart.key = data['key']
        chart.title = data['title']

        chart.x = data['x']
        chart.y = data['y']
        chart.w = data['w']
        chart.h = data['h']

        chart.x_p = data['x_p']
        chart.y_p = data['y_p']
        chart.w_p = data['w_p']
        chart.h_p = data['h_p']

        chart.kpi = data['kpi']
        chart.unified = data['unified']
        chart.unified_color = data['unified_color']
        chart.kpi_color = data['kpi_color']
        chart.smooth = data['smooth']
        chart.pie_type = data['pie_type']
        chart.is_client = data['is_client']
        chart.start_date = data['start_date']
        chart.end_date = data['end_date']

        chart.meta = data['meta']
        chart.entities = json.dumps(data['entities'])

        chart.save()
        temp = model_to_dict(chart)
        temp['entities'] = json.loads(temp['entities'])

        return JsonResponse(temp, safe=False)
    return HttpResponse('Wrong request')
