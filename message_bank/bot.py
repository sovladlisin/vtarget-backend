import random
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from users.models import VkUser, ServiceRequest
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from think_bank.views import vk_request
import requests
from .models import MessageBankUnit
import datetime


class ResponseThen(HttpResponse):
    def __init__(self, data, then_callback, message, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback
        self.message = message

    def close(self):
        super().close()
        self.then_callback(self.message)


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
            text = message.get('message', None)
            print('MESSAGE', text)
            print('BIDY', message)

            user_id = text['from_id']
            filtered_users = VkUser.objects.all().filter(user_id=user_id)

            if filtered_users.count() == 0:
                send_message(
                    'К сожалению вы не зарегистрированы на нашем сервисе.\nДля регистрации пройдите по ссылке: http://ml.vtargete.ru:14291 ', user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)

            try:
                return ResponseThen('ok', proccess_message, text, status=200)
            except:
                send_message(
                    'К сожалению возникла ошибка, просим извенения за неудобства. Повторите ваш запрос через несколько минут', user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)
        return HttpResponse('ok', content_type="text/plain", status=200)
    return HttpResponse('ok', content_type="text/plain", status=200)


def proccess_message(m_body):
    fwd_messages = m_body.get('fwd_messages', None)
    reg_user_id = m_body.get('from_id', None)

    if fwd_messages is None:
        send_message('Нет прикрепленных сообщений', reg_user_id)

    for m in fwd_messages:
        c_m = collect_message(m)

        inner_fwd_messages = m['fwd_messages']
        inner_fwd_messages_list = []
        for m_2 in inner_fwd_messages:
            c_m_2 = collect_message(m_2)
            inner_fwd_messages_list.append(c_m_2)

        save_message = MessageBankUnit(
            date=datetime.datetime.now(),
            date_written=c_m['date'],
            body=json.dumps(c_m),
            fwd_body=json.dumps(inner_fwd_messages_list)
        )
        save_message.save()
        send_message('Успех', reg_user_id)


def collect_message(m):
    result = {}
    result['text'] = m['text']
    result['date'] = m['date']
    result['from_id'] = m['from_id']
    result['attachments'] = collect_attachments(m['attachments'])

    user_info = getVkUserInfo(result['from_id'])
    result['name'] = user_info['name']
    result['photo'] = user_info['photo']

    return result


def collect_attachments(attachments):
    result = []
    for a in attachments:
        att = {}
        att['type'] = a['type']
        if att['type'] == 'photo':
            att['photo'] = a['photo']['sizes'][-1]['url']
        result.append(att)
    pass


def send_message(message, user_id):
    community_token = 'ec944a7cbd5b2bd0f86a5b5096782dd0ada66e6d8dbb0903a3321dfd8787ee1849385d2b5126d5df28b62'
    rand = int(random.randint(-30000, 30000))
    answer = vk_request('post', 'messages.send', {
                        'peer_id': user_id, 'message': message, 'random_id': rand}, community_token, '5.131')
    print(answer)


def getVkUserInfo(user_id):
    try:
        user_data = vk_request('get', 'users.get', {
                               'user_ids': user_id, 'fields': 'photo_200'}, 'ec944a7cbd5b2bd0f86a5b5096782dd0ada66e6d8dbb0903a3321dfd8787ee1849385d2b5126d5df28b62', '5.124')['response'][0]

        result = {}

        result['vk_id'] = user_data['id']
        result['photo'] = user_data['photo_200']
        result['name'] = user_data['first_name'] + ' ' + user_data['last_name']

        return result
    except:
        return -1
