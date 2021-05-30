from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from users.models import VkUser
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from .views import add_post_to_db, vk_request, send_message
# Create your views here.
key = 'test_key_2138573p9148'
error_message = 'Прошу прощения, я не понимаю данную ссылку. \nВы можете добавлять посты исключительно из \"Вконтакте\". \n\nДля дополнительной информации напишите мне \"Помощь\".'


@csrf_exempt
def Bot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        type = data['type']
        if (type == 'confirmation'):
            return HttpResponse("fee33a9c")
        if (type == 'message_new'):
            message = data['object']
            user_id = message['user_id']

            filtered_users = VkUser.objects.all().filter(user_id=user_id)
            if filtered_users.count() == 0:
                send_message(
                    'К сожалению вы не зарегистрированы на нашем сервисе.\nДля регистрации пройдите по ссылке: http://ml.vtargete.ru:14291/ ', user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)

            user = filtered_users.first()
            text = message.get('body', None)
            attachments = message.get('attachments', None)

            if attachments is not None:
                if attachments[0]['type'] == 'wall':
                    wall = attachments[0]['wall']
                    post_id = str(wall['from_id']) + '_' + str(wall['id'])
                    answer = add_post_to_db(True, post_id, user.pk, text)

                    if answer.get('error', False):
                        if answer.get('message', 'o') == 'link':
                            send_message(error_message, user_id)
                        else:
                            send_message('Ошибка сервера', user_id)
                    else:
                        send_message('Пост успешно добавлен', user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)

            if text is not None:
                if text.lower() == 'помощь':
                    message = ''
                    message += 'Способы загрузки информации из постов в ваш личный банк:\n'
                    message += '1.Отправить прямую ссылку на запись, вида: https://vk.com/XXX?w=wallXXX\n2. Поделиться со мной записью в сообщении.\n\n'
                    message += 'Для добавления комментария к сохраненной записи, достаточно указать ваш комментарий через пробел после ссылки или в виде сообщения при действии \"Поделиться записью\".\n\n'
                    message += 'Информация, сохраняемая в ваш банк из прикрепленной записи: текст, изображения, документы.\n'
                    message += 'При удалении оригинального поста - будут удалены изображения и документы.\n\n'
                    message += 'При возникших проблемах можно написать моему разработчику: https://vk.com/id122058319'
                    send_message(message, user_id)
                    return HttpResponse('ok', content_type="text/plain", status=200)

                split = text.split(' ')

                if (len(split) == 2):
                    answer = add_post_to_db(
                        False, split[0], user.pk, split[1])

                if (len(split) > 2):
                    post_link = split[0]
                    split = split.pop(0)
                    text = ''
                    for i in split:
                        text += i
                    answer = add_post_to_db(False, post_link, user.pk, i)

                if (len(split) == 1):
                    answer = add_post_to_db(False, split[0], user.pk, None)

                if answer.get('error', False):
                    if answer.get('message', 'o') == 'link':
                        send_message(error_message, user_id)
                    else:
                        send_message('Ошибка сервера', user_id)
                else:
                    send_message('Пост успешно добавлен', user_id)
                return HttpResponse('ok', content_type="text/plain", status=200)
            return HttpResponse('ok', content_type="text/plain", status=200)
        return HttpResponse('ok', content_type="text/plain", status=200)
    return HttpResponse('ok', content_type="text/plain", status=200)
