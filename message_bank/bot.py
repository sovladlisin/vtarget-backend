import random
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from users.models import VkUser, ServiceRequest
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from think_bank.views import vk_request
import requests

import datetime
from .views import addDownloadRecord


class ResponseThen(HttpResponse):
    def __init__(self, data, then_callback, user_id, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback
        self.user_id = user_id

    def close(self):
        super().close()
        self.then_callback(self.user_id)


@csrf_exempt
def Bot(request):
    if request.method == 'POST':
        print(request.body.decode('utf-8'))

        data = json.loads(request.body)
        type = data['type']
        print(data)
        if (type == 'confirmation'):
            return HttpResponse("5c2d39ba")
        if (type == 'message_new'):
            message = data['object']
            text = message.get('body', None)
            print('MESSAGE', text)

            user_id = message['user_id']
            filtered_users = VkUser.objects.all().filter(user_id=user_id)

            if filtered_users.count() == 0:
                send_message(
                    'К сожалению вы не зарегистрированы на нашем сервисе.\nДля регистрации пройдите по ссылке: http://ml.vtargete.ru:14291 ', user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)

            try:
                return ResponseThen('ok', proccess_message, user_id, status=200)
            except:
                send_message(
                    'К сожалению возникла ошибка, просим извенения за неудобства. Повторите ваш запрос через несколько минут', user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)
        return HttpResponse('ok', content_type="text/plain", status=200)
    return HttpResponse('ok', content_type="text/plain", status=200)


def proccess_message(user_id):
    pass


def send_message(message, user_id):
    community_token = 'b80859e3d19b51d9c172b0b51c68f6824ee392617640be2f827ba1929f85d4c0ffe876e55e5f5d1dcbfb8'
    rand = int(random.randint(-30000, 30000))
    answer = vk_request('post', 'messages.send', {
                        'peer_id': user_id, 'message': message, 'random_id': rand}, community_token, '5.131')
    print(answer)
