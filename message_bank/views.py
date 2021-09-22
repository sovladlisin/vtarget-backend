from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from users.models import VkUser
from .models import MessageBankUnit
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
            temp['date_added'] = m.date_written
            temp['body'] = json.loads(m.body)
            temp['fwd_body'] = json.loads(m.body)
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
