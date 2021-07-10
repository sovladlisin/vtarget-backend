from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
import json
from .models import Chart, Cabinet
from users.models import VkUser


@csrf_exempt
def getCabinets(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)
        user = VkUser.objects.get(pk=user_id)
        cabinets = Cabinet.objects.all().filter(user=user)
        result = []
        for cabinet in cabinets:
            temp = model_to_dict(cabinet)
            temp['token'] = cabinet.user.token

            temp['secondary_user'] = None
            if cabinet.secondary_user is not None:
                temp['token'] = cabinet.secondary_user.token
                temp['secondary_user'] = model_to_dict(cabinet.secondary_user)

            result.append(temp)
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def getCabinet(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        pk = data.get('id', None)
        cabinet = Cabinet.objects.get(pk=pk)
        result = model_to_dict(cabinet)
        result['token'] = cabinet.user.token

        result['secondary_user'] = None
        if cabinet.secondary_user is not None:
            result['token'] = cabinet.secondary_user.token
            result['secondary_user'] = model_to_dict(cabinet.secondary_user)

        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def createCabinet(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user = VkUser.objects.get(pk=data['user'])
        secondary_user_pk = data.get('secondary_user_pk', None)

        new_cabinet = Cabinet(
            title=data['title'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            changing_interval=data['changing_interval'],
            user=user
        )

        if secondary_user_pk is not None:
            secondary_user = VkUser.objects.get(pk=secondary_user_pk)
            new_cabinet.secondary_user = secondary_user

        new_cabinet.save()
        new_cabinet.token = user.token

        response = model_to_dict(new_cabinet)
        response['token'] = new_cabinet.user.token

        if new_cabinet.secondary_user is not None:
            response['token'] = new_cabinet.secondary_user.token
            response['secondary_user'] = model_to_dict(
                new_cabinet.secondary_user)

        return JsonResponse(response, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def deleteCabinet(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        cabinet = Cabinet.objects.get(pk=data['id'])
        cabinet.delete()
        return HttpResponse('Success')
    return HttpResponse('Wrong request')


@csrf_exempt
def updateCabinet(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        cabinet = Cabinet.objects.get(pk=data['id'])

        cabinet.title = data['title']
        cabinet.start_date = data['start_date']
        cabinet.end_date = data['end_date']
        cabinet.changing_interval = data['changing_interval']
        cabinet.save()

        cabinet.save()
        cabinet.token = cabinet.user.token

        response = model_to_dict(cabinet)
        response['token'] = cabinet.user.token

        if cabinet.secondary_user is not None:
            response['token'] = cabinet.secondary_user.token
            response['secondary_user'] = model_to_dict(
                cabinet.secondary_user)
        return JsonResponse(response, safe=False)
    return HttpResponse('Wrong request')
