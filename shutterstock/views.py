from datetime import datetime, timedelta
from json.decoder import JSONDecodeError
from dateutil.relativedelta import relativedelta
import datetime as dt
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from think_bank.views import vk_request
from django.db.models import Q
from users.models import VkUser
from .models import PhotostockAccount, UserDownloadRecords
import requests


# Create your views here.


@csrf_exempt
def shutterstockLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)
        url = data.get('url', None)
        if user_id is not None:
            user = VkUser.objects.get(pk=user_id)
            params = {
                "scope": "licenses.create licenses.view purchases.view",
                "state": "demo_" + '1243',
                "response_type": "code",
                "redirect_uri": url,
                "client_id": 'GejJmSWrI6Yz3Jvnwze04wxMVumFz62f'
            }
            r = requests.get(
                'https://api.shutterstock.com/v2/oauth/authorize', params, allow_redirects=False)

            return HttpResponse(r.headers['Location'])
    return HttpResponse('Wrong request')


@ csrf_exempt
def connectShutterstock(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)
        code = data.get('code', None)
        if user_id is not None:
            user = VkUser.objects.get(pk=user_id)

            params = {
                "client_id": 'GejJmSWrI6Yz3Jvnwze04wxMVumFz62f',
                "client_secret": 'RJ83FxIUSDDMNGG6',
                "grant_type": "authorization_code",
                "expires": 'false',
                "code": code
            }
            r = requests.post(
                "https://api.shutterstock.com/v2/oauth/access_token", params).json()
            if r.get('message', None) is not None:
                return HttpResponse('authorization_code not authorized')
            print(r)
            token = r.get('access_token', None)
            if token is None:
                return HttpResponse('Error')
            user.shutterstock_token = token
            user.save()
            user.shutterstock_token = True
            return JsonResponse(model_to_dict(user), safe=False)
    return HttpResponse('Wrong request')


@ csrf_exempt
def disconnectShutterstock(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)
        if user_id is not None:
            user = VkUser.objects.get(pk=user_id)
            user.shutterstock_token = ''
            user.save()
            user.shutterstock_token = False
            return JsonResponse(model_to_dict(user), safe=False)
    return HttpResponse('Wrong request')


@ csrf_exempt
def createPhotostockAccount(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username', None)
        password = data.get('password', None)
        stock_type = data.get('stock_type', None)
        if username is not None and password is not None and stock_type is not None:
            new_account = PhotostockAccount(
                username=username, password=password, stock_type=stock_type)
            new_account.save()
            new_account.password = True
            return JsonResponse(model_to_dict(new_account), safe=False)
        return HttpResponse('Wrong form')
    return HttpResponse('Wrong request')


@ csrf_exempt
def editPhotostockAccount(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        pk = data.get('pk', None)
        username = data.get('username', None)
        password = data.get('password', None)
        if username is not None and password is not None and pk is not None:
            new_account = PhotostockAccount.objects.get(pk=pk)
            new_account.password = password
            new_account.username = username
            new_account.save()
            new_account.password = True
            return JsonResponse(model_to_dict(new_account), safe=False)
        return HttpResponse('Wrong form')
    return HttpResponse('Wrong request')


@ csrf_exempt
def deletePhotostockAccount(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        pk = data.get('pk', None)
        if pk is not None:
            new_account = PhotostockAccount.objects.get(pk=pk)
            new_account.delete()
            return HttpResponse('ok')
        return HttpResponse('Wrong form')
    return HttpResponse('Wrong request')


@ csrf_exempt
def getPhotostockAccounts(request):
    if request.method == 'GET':
        result = []
        for account in PhotostockAccount.objects.all():
            account.password = True
            result.append(model_to_dict(account))
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@ csrf_exempt
def activatePhotostockAccount(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        pk = data.get('pk', None)
        if pk is not None:
            target_account = PhotostockAccount.objects.get(pk=pk)
            target_account.active = True
            target_account.save()

            for account in PhotostockAccount.objects.all().filter(stock_type=target_account.stock_type):
                if account.pk != pk:
                    account.active = False
                    account.save()

            return HttpResponse('OK')
        return HttpResponse('Not found')
    return HttpResponse('Wrong request')


def addDownloadRecord(date, dates):

    def delay_time(time_str, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
        if type(time_str) == str:
            time_str = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        ret = time_str + relativedelta(years=years, months=months,
                                       days=days, hours=hours, minutes=minutes, seconds=seconds)
        return ret

    last = delay_time(datetime.now(), months=-1)
    last_month = int(last.strftime("%s"))
    today = int(date.strftime("%s"))

    dates_array = json.loads(dates)

    dates_array.append(today)
    dates_array = list(filter(lambda x: x > last_month, dates_array))

    return json.dumps(dates_array)


@ csrf_exempt
def getDownloadRecords(request):
    if request.method == 'GET':
        result = []
        records = UserDownloadRecords.objects.all()

        for r in records:
            temp = {}
            temp['dates'] = json.loads(r.dates)
            temp_user = model_to_dict(r.user)
            temp_user['token'] = ''
            temp_user['post_token'] = ''
            temp_user['shutterstock_token'] = ''
            temp['user'] = temp_user
            result.append(temp)
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')
