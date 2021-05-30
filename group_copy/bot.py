from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from users.models import VkUser
from .models import CreatedGroup, FutureModerator
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from scheduler.views import vk_request


@csrf_exempt
def Bot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        type_ = data['type']
        print(data)
        group_id = data['group_id']

        created_group = CreatedGroup.objects.all().filter(group_id=group_id)
        if created_group.count == 0:
            return HttpResponse('ok', content_type="text/plain", status=200)

        created_group = created_group.first()

        if (type_ == 'confirmation'):
            return HttpResponse(created_group.code)

        if created_group.number_of_moderators == 0:
            created_group.delete()
            return HttpResponse('ok', content_type="text/plain", status=200)

        if (type_ == 'group_join'):
            user_id = data['object']['user_id']

            future_moderator = FutureModerator.objects.all().filter(vk_id=str(user_id))
            if future_moderator.count() == 0:
                return HttpResponse('ok', content_type="text/plain", status=200)
            fm = future_moderator.first()
            r = vk_request('get', 'groups.editManager', {
                           'group_id': int(group_id), 'user_id': int(user_id), 'role': fm.role, 'is_contact': fm.is_contact}, created_group.user.post_token, '5.126')
            print(r)
            fm.delete()
            created_group.number_of_moderators = created_group.number_of_moderators - 1
            if created_group.number_of_moderators == 0:
                created_group.delete()
            else:
                created_group.save()

            # {'type': 'group_join', 'object': {'user_id': 122058319, 'join_type': 'join'}, 'group_id': 201209616, 'event_id': '9bf488a8a9bcf752f8c4b799856654e28bb74b7f'}

        return HttpResponse('ok', content_type="text/plain", status=200)
    return HttpResponse('ok', content_type="text/plain", status=200)
