from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from users.models import VkUser
from .models import MessageBankUnit, MessageBankRepostPermission
from django.http import JsonResponse

import json
# Create your views here.


@csrf_exempt
def getMessages(request):
    if request.method == 'GET':
        messages = MessageBankUnit.objects.all()
        result = []
        for m in messages:
            temp = {}
            temp['date'] = m.date
            temp['id'] = m.pk
            temp['date_written'] = m.date_written
            temp['body'] = json.loads(m.body)
            temp['fwd_body'] = json.loads(m.fwd_body)
            result.append(temp)

        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def deleteMessage(request):
    if request.method == 'DELETE':
        pk = request.GET.get('id', None)
        if None in [id]:
            return HttpResponse(status=403)

        m = MessageBankUnit.objects.get(pk=pk)
        m.delete()

        return HttpResponse(status=200)
    return HttpResponse('Wrong request')


@csrf_exempt
def updateUserPermission(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        user_pk = data.get('user_pk', None)
        is_allowed = data.get('is_allowed', None)

        if None in [user_pk, is_allowed]:
            return HttpResponse(status=400)

        user = VkUser.objects.get(pk=user_pk)

        perms = MessageBankRepostPermission.objects.all().filter(user=user)
        if perms.count() == 0:
            perm = MessageBankRepostPermission(
                user=user, is_allowed=is_allowed)
        else:
            perm = perms.first()
            perm.is_allowed = is_allowed

        perm.save()

        response = {}
        response['user_id'] = user.user_id
        response['user_img'] = user.user_img
        response['user_name'] = user.user_name
        response['user_pk'] = user.pk
        response['id'] = perm.pk
        response['is_allowed'] = perm.is_allowed

        return JsonResponse(response, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def getUserPermissions(request):
    if request.method == 'GET':

        perms = MessageBankRepostPermission.objects.all()

        response = []

        for perm in perms:
            temp = {}
            temp['user_id'] = perm.user.user_id
            temp['user_img'] = perm.user.user_img
            temp['user_name'] = perm.user.user_name
            temp['user_pk'] = perm.user.pk
            temp['id'] = perm.pk
            temp['is_allowed'] = perm.is_allowed
            response.append(temp)

        return JsonResponse(response, safe=False)
    return HttpResponse('Wrong request')
