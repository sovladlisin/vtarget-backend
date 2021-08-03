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
# Create your views here.
# message = {date: '', message: '', user: ''}
import string
import random
from .models import OKUserPermissions


@csrf_exempt
def getUserById(request):
    if request.method == 'GET':
        user_pk = request.GET.get('user_pk', None)
        if user_pk is None:
            return HttpResponse(status=404)

        user = VkUser.objects.get(pk=user_pk)
        if user is None:
            return HttpResponse(status=404)

        perms = OKUserPermissions.objects.all().filter(user__pk=user.pk)

        user_perms = None
        if perms.count() == 0:
            user_perms = OKUserPermissions(user=user)
            user_perms.save()
        else:
            user_perms = perms.first()

        response = {}
        response['user_pk'] = user_pk
        response['permissions'] = json.loads(user_perms.permissions)

        return JsonResponse(response, safe=False)
    return HttpResponse('Wrong request')
