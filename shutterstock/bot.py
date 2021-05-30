import random
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from users.models import VkUser, ServiceRequest
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from think_bank.views import vk_request
import requests
from .models import PhotostockAccount, UserDownloadRecords
from .models import NewUser
import datetime
from .views import addDownloadRecord
from dateutil.relativedelta import relativedelta

PHOTO_URL = 'http://shutterstock.parsers.services.vtargete.ru:14292'
# PHOTO_URL = 'http://138.201.123.31:14292'
PERSONAL_IMAGES_LIMIT = 70


class ResponseThen(HttpResponse):
    def __init__(self, data, then_callback, url, user_id, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback
        self.url = url
        self.user_id = user_id

    def close(self):
        super().close()
        self.then_callback(self.url, self.user_id)


# Create your views here.
key = 'test_key_2138573p9148'
error_message = 'Прошу прощения, я не понимаю данную ссылку. \nВы можете добавлять посты исключительно из \"Вконтакте\". \n\nДля дополнительной информации напишите мне \"Помощь\".'


def delay_time(time_str, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
    if type(time_str) == str:
        time_str = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    ret = time_str + relativedelta(years=years, months=months,
                                   days=days, hours=hours, minutes=minutes, seconds=seconds)
    return ret


@csrf_exempt
def Bot(request):
    if request.method == 'POST':
        print(request.body)
        print(request)
        print(request.body.decode('utf-8'))

        data = json.loads(request.body)
        type = data['type']
        print(data)
        if (type == 'confirmation'):
            return HttpResponse("8e91207a")
        if (type == 'message_new'):
            # return HttpResponse('ok', content_type="text/plain", status=200)
            message = data['object']
            text = message.get('body', None)
            user_id = message['user_id']
            filtered_users = VkUser.objects.all().filter(user_id=user_id)
            if text.lower() == 'помощь':
                message = ''
                message += 'Для загрузки изображения с shutterstock или depositphotos, напишите сообщение вида: скачать <ссылка>.\n'
                message += 'Бот принимает только одну ссылку на сообщение.\n'
                message += 'Пожалуйста не отправляйте новых ссылок, пока бот не обработал ваш предыдущий запрос.'
                send_message(message, user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)

            if ('shutter' in text.lower()) or ('deposit' in text.lower()):
                if filtered_users.count() == 0:
                    if NewUser.objects.all().filter(user_id=user_id) == 0:
                        new_user = NewUser(user_id=user_id)
                        new_user.save()
                        send_message(
                            'Здравствуйте, это сообщение было создано автоматически. Для вашего удобства был создан чат-бот, способный обрабатывать ваши запросы на скачивание фотографий в течении пары минут. Для его использования, вы можете зарегистрироваться на нашем сервисе: http://ml.vtargete.ru:14291 . После регистрации, вы можете подать заявку на использование нашего сервиса. После одобрения заявки, напишите в чат "помощь". Оповещение об одобрении заявки поступит в текущий чат.', user_id)
                        return HttpResponse('ok', content_type="text/plain", status=200)

            if 'скачать' not in text.lower():
                return HttpResponse('ok', content_type="text/plain", status=200)

            if 'shutterstock.com' not in text.lower():
                if 'https://ru.depositphotos.com/' not in text.lower():
                    return HttpResponse('ok', content_type="text/plain", status=200)

            if filtered_users.count() == 0:
                send_message(
                    'К сожалению вы не зарегистрированы на нашем сервисе.\nДля регистрации пройдите по ссылке: http://ml.vtargete.ru:14291 ', user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)

            user = filtered_users.first()

            authorize = user.is_admin
            autorize_set = ServiceRequest.objects.all().filter(
                service_id=5, is_accepted=True, user=user)
            if autorize_set.count() != 0:
                application = autorize_set.first()
                d1 = application.date_until
                d2 = datetime.date.today()
                if d1 > d2:
                    authorize = True
                else:
                    application.is_accepted = False
                    application.is_pending = True
                    application.is_denied = False
                    application.save()

            if authorize == False:
                send_message(
                    'К сожалению у вас нет прав для пользования сервисом скачивания фотографий. Для получения доступа оставьте заявку на сайте нашего сервиса. При долгом рассмотрении заявки напишите Константину Крестинину.', user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)

            now_d = delay_time(datetime.date.now(), days=10)
            if user.date_shutter_banned > now_d.date():
                send_message(
                    'Лимит изображений на персональном аккаунте исчерпанна 10 дней.', user_id)
                return None

            requested_image_url = text.split(' ')[1]

            try:
                return ResponseThen('ok', proccess_img, requested_image_url, user_id, status=200)
            except:
                send_message(
                    'К сожалению возникла ошибка, просим извенения за неудобства. Повторите ваш запрос через несколько минут', user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)
        return HttpResponse('ok', content_type="text/plain", status=200)
    return HttpResponse('ok', content_type="text/plain", status=200)


def send_message(message, user_id):
    community_token = 'b80859e3d19b51d9c172b0b51c68f6824ee392617640be2f827ba1929f85d4c0ffe876e55e5f5d1dcbfb8'
    rand = random.randint(-32768, 32767)
    answer = vk_request('get', 'messages.send', {
                        'peer_id': user_id, 'message': message, 'random_id ': rand}, community_token, '5.45')
    print(answer)


def proccess_img(url, user_id, times=4):
    print('start_gg')
    if times == 0:
        send_message(
            'Просим прощения, данное изображение не входит в лицензию/на сервере произошла ошибка/все подписки исчерпаны. Повторите запрос через 30 минут.', user_id)
        return None

    if times == 4:
        send_message(
            'Спасибо за запрос. Ваша ссылка будет доступна в течении пары минут. Пожалуйста не отправляйте новых ссылок, пока бот не обработал ваш предыдущий запрос. Если ответ на ваш запрос не поступил в течении 10 минут, пожалуйста, повторите запрос.', user_id)

    if 'shutter' in url.lower():
        sh_id = 's' + url.split('-')[-1]
    if 'deposit' in url.lower():
        sh_id = 'd' + url.split('/')[3]

    existed = requests.post(
        PHOTO_URL + '/api/get_tags_of_image', data=json.dumps({'sh_id': sh_id})).json()
    if existed['response'] != 'image not found':
        ex_url = existed['response'].get('url', None)
        result_url = PHOTO_URL + \
            str(ex_url)
        send_message('Спасибо за ожидание. Изображение было взято из нашего банка. Ссылка на изображение №' +
                     sh_id + ': ' + result_url, user_id)

    else:

        photostock_account = None
        if sh_id[0] == 'd':
            for acc in PhotostockAccount.objects.all().filter(active=True, stock_type=2):
                photostock_account = acc

        if sh_id[0] == 's':
            for acc in PhotostockAccount.objects.all().filter(active=True, stock_type=1):
                photostock_account = acc

        request_url = 'http://parser3.soso.ru.com/api/putfile' if sh_id[
            0] == 's' else 'http://parser4.soso.ru.com/api/putfile'
        print(request_url, url, photostock_account.username,
              photostock_account.password)

        try:
            t = requests.post(request_url, {
                              'url_download': url, 'login': photostock_account.username, 'password': photostock_account.password}, timeout=240).json()
        except:
            proccess_img(url, user_id, times=times-1)
            return None

        print(t)

        tags = t.get('tags', [])
        img_file = t.get('file', None)
        available_downloads = t.get('available_downloads', None)
        rest_of_days = t.get('rest_of_days', None)

        if available_downloads is not None:
            photostock_account.available_downloads = int(available_downloads)

        if rest_of_days is not None:
            photostock_account.rest_of_days = int(rest_of_days)

        photostock_account.save()

        # switching
        if photostock_account.available_downloads == 0:
            photostock_account.active = False
            photostock_account.save()

            for acc in PhotostockAccount.objects.all().filter(stock_type=photostock_account.stock_type):
                if acc.pk != photostock_account.pk:
                    acc.active = True
                    acc.save()

            send_message(
                'Лимит изображений на аккаунте исчерпан. Меняем аккаунт...', user_id)

        if img_file is not None:

            filtered_users = VkUser.objects.all().filter(user_id=user_id)
            if filtered_users[0] is not None:
                current_user = filtered_users[0]
                current_record = UserDownloadRecords.objects.filter(
                    user=current_user).first()
                if current_record is not None:
                    current_record.dates = addDownloadRecord(
                        datetime.datetime.now(), current_record.dates)
                    current_record.save()
                else:
                    current_record = UserDownloadRecords(
                        user=current_user, dates='[]')
                    current_record.dates = addDownloadRecord(
                        datetime.datetime.now(), current_record.dates)
                    current_record.save()

            for acc in PhotostockAccount.objects.all().filter(stock_type=photostock_account.stock_type):
                if acc.pk != photostock_account.pk:
                    acc.active = False
                    acc.save()

            data = {
                'sh_id': sh_id,
                'url': img_file,
                'tags': tags
            }
            r = requests.post(
                PHOTO_URL + '/api/add_image', data=json.dumps(data))
            existed_new = requests.post(
                PHOTO_URL + '/api/get_tags_of_image', data=json.dumps({'sh_id': sh_id})).json()
            result_url = PHOTO_URL + \
                str(existed_new['response']['url'])

            send_message('Спасибо за ожидание. Дней в лицензии: ' + str(rest_of_days) + '. Осталось загрузок: ' + str(int(available_downloads) - 1) + '. Ссылка на изображение №' +
                         str(sh_id) + ': ' + str(result_url), user_id)

        else:
            proccess_img(url, user_id, times=times-1)
