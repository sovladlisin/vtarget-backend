from django.shortcuts import render
from .models import PlannedPost, AvailableGroup, SavedPost
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from think_bank.views import vk_request
from django.db.models import Q

from users.models import VkUser
# Create your views here.


@csrf_exempt
def addPlannedPosts(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        target_groups_id = data.get('target_groups_id', None)
        post = data.get('post', None)

        from_group = data.get('from_group', 1)
        mark_as_ads = data.get('mark_as_ads', 0)
        close_comments = data.get('close_comments', 0)
        mute_notifications = data.get('mute_notifications', 0)

        time_add = data.get('time_add', None)
        time_delete = data.get('time_delete', None)

        every_day_marker = data.get('every_day_marker', None)

        days_add = data.get('days_add', None)
        days_delete = data.get('days_delete', None)

        timestamp = data.get('timestamp', None)

        if data is not None:
            post = SavedPost.objects.get(pk=post)
            new_planned_post = PlannedPost(
                post=post,
                target_groups_id=target_groups_id,

                from_group=int(from_group),
                mark_as_ads=int(mark_as_ads),
                close_comments=int(close_comments),
                mute_notifications=int(mute_notifications),

                time_add=time_add,
                time_delete=time_delete,

                every_day_marker=every_day_marker,

                days_add=days_add,
                days_delete=days_delete,
            )
            new_planned_post.save()
            return JsonResponse(model_to_dict(new_planned_post), safe=False)
        return HttpResponse('404')
    return HttpResponse('Wrong request')


@csrf_exempt
def getPlannedPosts(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('user_id', None)
        if id is not None:
            posts = PlannedPost.objects.all().filter(post__user__pk=id)
            result = []
            for post in posts:
                result.append(model_to_dict(post))
            return JsonResponse(result, safe=False)
        return HttpResponse('404')
    return HttpResponse('Wrong request')


@csrf_exempt
def getAvailableGroups(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)
        if user_id is not None:
            groups = AvailableGroup.objects.all().filter(user__pk=user_id)
            result = []
            for group in groups:
                result.append(model_to_dict(group))
            return JsonResponse(result, safe=False)
        return HttpResponse('404')
    return HttpResponse('Wrong request')


@csrf_exempt
def addAvailableGroup(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        user_id = data.get('user_id', None)
        group_url = data.get('group_url', None)

        if user_id is not None and group_url is not None:
            user = VkUser.objects.get(pk=user_id)

            if 'https://vk.com/' in group_url:
                processed_url = group_url.replace('https://vk.com/', '')
                if 'public' in processed_url:
                    processed_url = processed_url.replace('public', '')
            else:
                return {'error': True, 'message': 'not_url'}

            if AvailableGroup.objects.all().filter(Q(user=user) & Q(group_id=processed_url)).count() == 0:
                group = vk_request('get', 'groups.getById', {
                    'group_ids': processed_url}, user.token, '5.124')['response'][0]

                new_group = AvailableGroup(
                    group_id=group['id'], name=group['name'], group_img=group['photo_50'], user=user)
                new_group.save()
                return JsonResponse(model_to_dict(new_group), safe=False)

    return HttpResponse('Wrong request')


@csrf_exempt
def deleteAvailableGroup(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)
        if id is not None:
            group = AvailableGroup.objects.get(pk=id)
            planned_posts = PlannedPost.objects.all()
            for post in planned_posts:
                ids = json.loads(post.target_groups_id)
                if id in ids:
                    post.delete()
            group.delete()
            return HttpResponse('Success')
        return HttpResponse('404')
    return HttpResponse('Wrong request')


@csrf_exempt
def deletePlannedPost(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)
        if id is not None:
            post = PlannedPost.objects.get(id=id)
            post.delete()
            return HttpResponse('Success')
        return HttpResponse('404')
    return HttpResponse('Wrong request')


@csrf_exempt
def addSavedPost(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)
        post_link = data.get('post_link', None)

        if user_id is not None and post_link is not None:
            user = VkUser.objects.all().get(pk=user_id)

            if 'wall' in post_link:
                if '-' in post_link:
                    splitted = post_link.split('-')
                    post_id = splitted[1]
                    post_id = "-" + post_id
                else:
                    splitted = post_link.split('wall')[1]
                    post_id = splitted.split('?')[0]
            else:
                return {'error': True, 'message': 'link'}

            wall_data = vk_request('get', 'wall.getById', {
                'posts': post_id}, user.token, '5.124')['response'][0]
            print(wall_data)
            new_post = SavedPost(user=user,
                                 message=wall_data['text'],
                                 attachments=json.dumps(wall_data.get('attachments', '')))
            new_post.save()
            return JsonResponse(model_to_dict(new_post), safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def getSavedPosts(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)
        if user_id is not None:
            posts = SavedPost.objects.all().filter(user__pk=user_id)
            result = []
            for post in posts:
                result.append(model_to_dict(post))
            return JsonResponse(result, safe=False)
        return HttpResponse('404')
    return HttpResponse('Wrong request')


@csrf_exempt
def deleteSavedPost(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)
        if id is not None:
            post = SavedPost.objects.get(pk=id)
            post.delete()
            return HttpResponse('Success')
        return HttpResponse('404')
    return HttpResponse('Wrong request')
