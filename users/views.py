from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from .models import VkUser, ServiceInfo
from think_bank.views import vk_request
import requests
from .models import ServiceRequest
from shutterstock.bot import send_message
# client_id = '7613764'
client_id = '7647441'

# client_secret = 'B9MxUsRKbMNCWwvJgIPM'
client_secret = 'ClAXUPylS1FBGWxw6y2n'


@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        user_id = user.get('user_id', None)
        token = user.get('access_token', None)
        # redirect_url = user.get('url', None)
        if token is not None:

            # r = requests.get(
            #     'https://oauth.vk.com/access_token?client_id='+client_id+'&client_secret='+client_secret+'&redirect_uri='+redirect_url+'&code=' + code)
            # result = json.loads(r.content.decode('utf-8'))

            # token = result['access_token']
            # user_id = result['user_id']

            users = VkUser.objects.all().filter(user_id=user_id)
            if not users:
                user_data = vk_request('get', 'users.get', {
                                       'user_ids': user_id, 'fields': 'photo_200'}, token, '5.124')['response'][0]
                new_user = VkUser(
                    user_id=user_data['id'], user_img=user_data['photo_200'], user_name=user_data['first_name'] + ' ' + user_data['last_name'], token=token, post_token='')
                new_user.save()
                new_user.post_token = ''
                new_user.shutterstock_token = ''
                result = model_to_dict(new_user)
                result['medals'] = json.loads(new_user.medals)
                return JsonResponse(result, safe=False)
            else:
                old_user = users.first()
                old_user.token = token
                old_user.save()
                result = model_to_dict(old_user)
                result['medals'] = json.loads(old_user.medals)
                return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def addPostToken(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        user_id = user.get('user_id', None)
        token = user.get('access_token', None)
        if token is not None:
            users = VkUser.objects.all().filter(user_id=user_id)
            if not users:
                return HttpResponse('404')
            user = users.first()
            user.post_token = token
            user.save()
            user.post_token = True
            return JsonResponse(model_to_dict(user), safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def deletePostToken(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        user_id = user.get('id', None)
        if user_id is not None:
            user = VkUser.objects.get(pk=user_id)
            user.post_token = ''
            user.save()
            user.post_token = False
            return JsonResponse(model_to_dict(user), safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def getServiceRequests(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        user_id = user.get('user_pk', None)
        if user_id is not None:
            user = VkUser.objects.get(pk=user_id)
            if user.is_admin:
                result = []
                for r in ServiceRequest.objects.all():
                    result.append(model_to_dict(r))
                return JsonResponse(result, safe=False)
            result = []
            for r in ServiceRequest.objects.all().filter(user__pk=user_id):
                result.append(model_to_dict(r))
            return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def toggleUserAdminRole(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        admin_pk = user.get('admin_pk', None)
        user_pk = user.get('user_pk', None)
        if user_pk is not None and admin_pk is not None:
            user = VkUser.objects.get(pk=user_pk)
            admin = VkUser.objects.get(pk=admin_pk)
            if admin.is_admin:
                if admin.pk == user.pk:
                    return HttpResponse('ok', status=200)
                user.is_admin = False if user.is_admin == True else True
                user.save()
                return HttpResponse('ok', status=200)
    return HttpResponse('Wrong request')


@csrf_exempt
def applyServiceRequest(request):

    services = [{'name': 'Банк креативов', 'id': 1, 'link': '/think-bank'},
                {'name': 'Планировщик публикаций', 'id': 2, 'link': '/scheduler'},
                {'name': 'Клонировщик групп', 'id': 3, 'link': '/copy-group'},
                {'name': 'Статистика проектов', 'id': 4, 'link': '/diagrams'},
                {'name': 'Изображения фотостоков',
                    'id': 5, 'link': '/shutterstock'},
                {'name': 'Калькуляторы', 'id': 6, 'link': '/calc'},
                {'name': 'Генератор идей', 'id': 7, 'link': '/idea-generator'},
                {'name': 'Чат', 'id': 8, 'link': '/chat'},
                {'name': 'Сертификаты', 'id': 9, 'link': '/certificates'},
                {'name': 'Статистика приложений Vk',
                    'id': 10, 'link': '/app_stat'},
                {'name': 'Таблицы Excel', 'id': 11, 'link': '/excel_tables'},
                {'name': 'Клоны страниц', 'id': 12, 'link': '/account_duplicates'},
                {'name': 'ОК кабинеты', 'id': 13, 'link': '/ok_cabinets'},
                {'name': 'Банк сообщений', 'id': 14, 'link': '/message_bank'},
                ]

    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        user_id = user.get('user_pk', None)
        service_id = user.get('service_id', None)
        if user_id is not None:
            user = VkUser.objects.get(pk=user_id)

            # send message to administration
            service_name = ''
            for service in services:
                if service['id'] == service_id:
                    service_name = service['name']
            admin_id = '374982599'
            # admin_id = '122058319'
            send_message('Пользователь ' + user.user_name +
                         ' запрашивает доступ к сервису ' + service_name + '. Ссылка в личный кабинет: http://ml.vtargete.ru:14291/account', admin_id)

            new_application = ServiceRequest(
                user=user, service_id=service_id, is_pending=True, is_accepted=False, is_denied=False)
            new_application.save()
            return JsonResponse(model_to_dict(new_application), safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def acceptServiceRequest(request):
    services = [{'name': 'Банк креативов', 'id': 1, 'link': '/think-bank'},
                {'name': 'Планировщик публикаций', 'id': 2, 'link': '/scheduler'},
                {'name': 'Клонировщик групп', 'id': 3, 'link': '/copy-group'},
                {'name': 'Статистика проектов', 'id': 4, 'link': '/diagrams'},
                {'name': 'Изображения фотостоков',
                    'id': 5, 'link': '/shutterstock'},
                {'name': 'Калькуляторы', 'id': 6, 'link': '/calc'},
                {'name': 'Генератор идей', 'id': 7, 'link': '/idea-generator'},
                {'name': 'Чат', 'id': 8, 'link': '/chat'},
                {'name': 'Сертификаты', 'id': 9, 'link': '/certificates'},
                {'name': 'Статистика приложений Vk',
                    'id': 10, 'link': '/app_stat'},
                {'name': 'Таблицы Excel', 'id': 11, 'link': '/excel_tables'},
                {'name': 'Клоны страниц', 'id': 12, 'link': '/account_duplicates'},
                {'name': 'ОК кабинеты', 'id': 13, 'link': '/ok_cabinets'},
                {'name': 'Банк сообщений', 'id': 14, 'link': '/message_bank'},
                ]

    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        request_pk = user.get('id', None)
        date_until = user.get('date', None)
        if request_pk is not None:
            application = ServiceRequest.objects.get(pk=request_pk)

            application.is_pending = False
            application.is_accepted = True
            application.is_denied = False
            application.date_until = date_until
            application.save()

            service_name = ''
            for service in services:
                if service['id'] == application.service_id:
                    service_name = service['name']

            send_message('Вам дан доступ к  ' + service_name,
                         application.user.user_id)

            return JsonResponse(model_to_dict(application), safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def denyServiceRequest(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        request_pk = user.get('id', None)
        if request_pk is not None:
            application = ServiceRequest.objects.get(pk=request_pk)
            application.is_pending = False
            application.is_accepted = False
            application.is_denied = True
            application.save()
            return JsonResponse(model_to_dict(application), safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def checkServiceRequest(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        request_pk = user.get('id', None)
        if request_pk is not None:
            application = ServiceRequest.objects.get(pk=request_pk)
            if application.is_accepted:
                d1 = application.date_until
                d2 = datetime.date.today()
                if d1 > d2:
                    return JsonResponse(model_to_dict(application), safe=False)
                application.is_pending = True
                application.is_denied = False
                application.is_accepted = False
                application.save()
                return JsonResponse(model_to_dict(application), safe=False)
            return JsonResponse(model_to_dict(application), safe=False)
        return HttpResponse('Not found')
    return HttpResponse('Wrong request')


@csrf_exempt
def editServiceInfo(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        text = data.get('text', None)
        service_id = data.get('service_id', None)
        if service_id is not None and text is not None:
            services = ServiceInfo.objects.filter(service_id=service_id)
            if not services:
                service = ServiceInfo(service_id=service_id, text=text)
                service.save()
            else:
                service = services.first()
                service.text = text
                service.save()
            return JsonResponse(model_to_dict(service), safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def getServiceInfo(request):
    if request.method == 'POST':
        result = []
        infos = ServiceInfo.objects.all()
        for info in infos:
            result.append(model_to_dict(info))
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def shutterBanUser(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_pk = data.get('user_pk', None)
        user = VkUser.objects.get(pk=user_pk)
        now = datetime.datetime.now()
        user.date_shutter_banned = now.date()
        user.save()
        return JsonResponse(model_to_dict(user), safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def shutterUnbanUser(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_pk = data.get('user_pk', None)
        user = VkUser.objects.get(pk=user_pk)
        user.date_shutter_banned = datetime.date(2009, 5, 3)
        user.save()
        return JsonResponse(model_to_dict(user), safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def getUserMedals(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_pk = data.get('user_pk', None)
        user = VkUser.objects.get(pk=user_pk)
        result = json.loads(user.medals)
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def getAllUsers(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        admin_pk = data.get('admin_pk', None)
        admin = VkUser.objects.get(pk=admin_pk)
        if admin.is_admin is False:
            return HttpResponse(status=403)

        result = []
        for user in VkUser.objects.all():
            temp = model_to_dict(user)
            temp['token'] = ''
            temp['post_token'] = ''
            temp['shutterstock_token'] = ''
            temp['medals'] = json.loads(user.medals)
            result.append(temp)

        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')
