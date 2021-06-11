from django.shortcuts import render
from datetime import date, datetime, timedelta
from json.decoder import JSONDecodeError
from dateutil.relativedelta import relativedelta
import datetime as dt
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from users.models import VkUser
from .models import ChatLog
# Create your views here.
# message = {date: '', message: '', user: ''}
import string
import random


@csrf_exempt
def getAllChatLogs(request):
    if request.method == 'GET':
        user_pk = request.GET.get('user_pk', None)
        if user_pk is None:
            return HttpResponse(status=404)

        all_chats = ChatLog.objects.all()
        owned = all_chats.filter(owner__pk=user_pk)

        owned_chats = []
        for c in owned:
            owned_chats.append({'key': c.key, 'name': c.name})

        return JsonResponse(owned_chats, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def getChatLog(request):
    if request.method == 'GET':
        key = request.GET.get('key', None)
        if key is None:
            return HttpResponse(status=404)
        chat_array = ChatLog.objects.all().filter(key=key)
        if chat_array.count() == 0:
            return HttpResponse(status=404)

        chat = chat_array.first()
        chat_log = json.loads(chat.log)
        result = {"owner": chat.owner.pk, "log": chat_log,
                  "key": chat.key, 'id': chat.pk, "name": chat.name}
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def deleteChatLog(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        key = data.get('key', None)
        user_pk = data.get('user_pk', None)
        if key is None:
            return HttpResponse(status=404)
        chat_array = ChatLog.objects.all().filter(key=key)
        if chat_array.count() == 0:
            return HttpResponse(status=404)
        chat = chat_array.first()

        if user_pk != chat.owner.pk:
            return HttpResponse(status=403)
        chat.delete()
        return HttpResponse(status=200)
    return HttpResponse('Wrong request')


@csrf_exempt
def createChatLog(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_pk = data.get('user_pk', None)
        name = data.get('name', None)
        owner = VkUser.objects.get(pk=user_pk)
        key = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=60))
        chat = ChatLog(key=key,
                       owner=owner, log='[]', name=name)
        chat.save()
        result = {'key': chat.key, 'name': chat.name}
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def postChatLog(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        key = data.get('key', None)
        user = data.get('user', None)
        message_text = data.get('message', None)
        if key is None:
            return HttpResponse(status=404)
        chat_array = ChatLog.objects.all().filter(key=key)
        if chat_array.count() == 0:
            return HttpResponse(status=404)
        chat = chat_array.first()
        print(user)
        message = {'user': user,
                   'message': message_text, 'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        log = json.loads(chat.log)
        log.append(message)
        chat.log = json.dumps(log)
        chat.save()
        return HttpResponse(status=200)
    return HttpResponse('Wrong request')
