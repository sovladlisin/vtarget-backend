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
            temp['date_added'] = m.date_written
            temp['body'] = json.loads(m.body)
            temp['fwd_body'] = json.loads(m.body)

        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')
