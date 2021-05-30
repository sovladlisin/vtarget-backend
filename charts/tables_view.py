from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
import json
from .models import Table, Cabinet


@csrf_exempt
def getTables(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        cabinet_id = data.get('cabinet_id', None)
        cabinet = Cabinet.objects.get(pk=cabinet_id)
        tables = Table.objects.all().filter(cabinet=cabinet)
        result = []
        for table in tables:
            temp = model_to_dict(table)
            temp['entities'] = json.loads(temp['entities'])
            temp['custom_keys'] = json.loads(temp['custom_keys'])
            result.append(temp)
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def createTable(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        cabinet = Cabinet.objects.get(pk=data['cabinet'])

        new_table = Table(
            cabinet=cabinet,
            is_public=data['is_public'],
            title=data['title'],

            x=data['x'],
            y=data['y'],
            w=data['w'],
            h=data['h'],

            x_p=data['x_p'],
            y_p=data['y_p'],
            w_p=data['w_p'],
            h_p=data['h_p'],

            is_collapsed=data['is_collapsed'],
            is_client_table=data['is_client_table'],

            custom_keys=json.dumps(data['custom_keys']),
            entities=json.dumps(data['entities'])
        )

        new_table.save()
        temp = model_to_dict(new_table)
        temp['entities'] = json.loads(temp['entities'])
        temp['custom_keys'] = json.loads(temp['custom_keys'])

        return JsonResponse(temp, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def deleteTable(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        table = Table.objects.get(pk=data['id'])
        table.delete()
        return HttpResponse('Success')
    return HttpResponse('Wrong request')


@csrf_exempt
def updateTable(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        table = Table.objects.get(pk=data['id'])
        table.is_public = data['is_public']
        table.title = data['title']

        table.x = data['x']
        table.y = data['y']
        table.w = data['w']
        table.h = data['h']

        table.x_p = data['x_p']
        table.y_p = data['y_p']
        table.w_p = data['w_p']
        table.h_p = data['h_p']

        table.is_collapsed = data['is_collapsed']
        table.is_client_table = data['is_client_table']

        table.custom_keys = json.dumps(data['custom_keys'])
        table.entities = json.dumps(data['entities'])

        table.save()
        temp = model_to_dict(table)
        temp['entities'] = json.loads(temp['entities'])
        temp['custom_keys'] = json.loads(temp['custom_keys'])

        return JsonResponse(temp, safe=False)
    return HttpResponse('Wrong request')
