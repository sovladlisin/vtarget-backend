from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.db.models import Q
from users.models import VkUser
from .models import Post, Comment, VkUserPermissions
import requests
import random
# Create your views here.


@csrf_exempt
def getPostsByUserId(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)
        if id is not None:
            posts = Post.objects.all().filter(user__pk=id)
            result = []
            for post in posts:
                d_post = model_to_dict(post)
                d_post['comments'] = []
                com = Comment.objects.filter(post=post)
                for c in com:
                    temp = d_post['comments']
                    temp.append(model_to_dict(c))
                    d_post['comments'] = temp
                result.append(d_post)
            return JsonResponse(result, safe=False)
        return HttpResponse('404')
    return HttpResponse('Wrong request')


@csrf_exempt
def getPostById(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)
        if id is not None:
            post = Post.objects.get(pk=id)
            d_post = model_to_dict(post)
            d_post['comments'] = []
            com = Comment.objects.filter(post=post)
            for c in com:
                temp = d_post['comments']
                temp.append(model_to_dict(c))
                d_post['comments'] = temp
            return JsonResponse(d_post, safe=False)
        return HttpResponse('404')
    return HttpResponse('Wrong request')


@csrf_exempt
def getPermissions(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)
        if id is not None:
            temp_user = VkUser.objects.get(pk=id)
            perms = VkUserPermissions.objects.all().filter(
                Q(owner=temp_user) | Q(viewer=temp_user))
            result = []
            for entry in perms:
                result.append(model_to_dict(entry))
            return JsonResponse(result, safe=False)
    return HttpResponse('Wrong type')


@csrf_exempt
def addPermission(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        owner = data.get('owner', None)
        viewer = data.get('viewer', None)
        if owner is not None:
            if viewer is not None:
                owner_obj = VkUser.objects.get(pk=owner)
                viewer_obj = VkUser.objects.get(pk=viewer)
                new_perm = VkUserPermissions(
                    owner=owner_obj, viewer=viewer_obj)
                new_perm.save()
                return JsonResponse(model_to_dict(new_perm))
    return HttpResponse('Wrong request')


@csrf_exempt
def deletePermission(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)
        if id is not None:
            perm = VkUserPermissions.objects.get(pk=id)
            perm.delete()
            return HttpResponse('Success')
    return HttpResponse('Wrong request')


@csrf_exempt
def getPostComments(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)
        if id is not None:
            result = []
            post = Post.objects.get(pk=id)
            comments = Comment.objects.all().filter(post=post)
            for comment in comments:
                user = model_to_dict(comment.user)
                temp = {'id': comment.pk, 'post': post.pk, 'user': user,
                        'comment': comment.comment, 'date': comment.date}
                result.append(temp)
            return JsonResponse(result, safe=False)
        return HttpResponse('404')
    return HttpResponse('Wrong request')


@csrf_exempt
def getUsers(request):
    users = VkUser.objects.all()
    result = []
    for user in users:
        user.token = True
        result.append(model_to_dict(user))
    return JsonResponse(result, safe=False)


@csrf_exempt
def getUser(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        id = user.get('id', None)
        if id is not None:
            user = VkUser.objects.get(pk=id)
            user.token = True
            return JsonResponse(model_to_dict(user), safe=False)
        return HttpResponse('404')
    return HttpResponse('Wrong request')


@csrf_exempt
def addPost(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        post_link = user.get('post_link', None)
        user_id = user.get('user_id', None)
        new_post = add_post_to_db(False, post_link, user_id, None)
        return JsonResponse(new_post, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def deletePost(request):
    if request.method == 'POST':
        user = json.loads(request.body.decode('utf-8'))
        post_id = user.get('id', None)
        if post_id is not None:
            del_post = Post.objects.get(pk=post_id)
            del_post.delete()
            return HttpResponse('Success')
        return HttpResponse(status=404)
    return HttpResponse('Wrong request')


@csrf_exempt
def addComment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        post_pk = data.get('post', None)
        user_pk = data.get('user', None)
        comment = data.get('comment', None)
        if post_pk is not None:
            post = Post.objects.get(pk=post_pk)
            if user_pk is not None:
                user = VkUser.objects.get(pk=user_pk)
                if comment is not None:
                    new_comment = Comment(user=user, comment=comment,
                                          post=post, date=datetime.datetime.now())
                    new_comment.save()
                    return JsonResponse(model_to_dict(new_comment), safe=False)
        return HttpResponse(status=404)
    return HttpResponse(status=403)


@csrf_exempt
def deleteComment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)
        if id is not None:
            del_comment = Comment.objects.get(pk=id)
            del_comment.delete()
            return HttpResponse('Success')
    return HttpResponse(status=403)


def vk_request(type, name, params, token, v):
    params['access_token'] = token
    params['v'] = v

    if type == 'get':
        r = requests.get('https://api.vk.com/method/' + name, params)
        return r.json()
    if type == 'post':
        r = requests.post('https://api.vk.com/method/' + name, params)
        return r.json()


def add_post_to_db(id_check, post_link, user_id, comment):
    user = VkUser.objects.all().get(pk=user_id)
    if id_check:
        post_id = post_link
    else:
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
    if post_id[0] == '-':
        owner = vk_request('get', 'groups.getById', {
            'group_ids': int(wall_data['owner_id']) * -1}, user.token, '5.124')['response'][0]
        owner_name = owner['name']
        owner_photo = owner['photo_50']
    else:
        owner = vk_request('get', 'users.get', {
            'user_ids': wall_data['owner_id'], 'fields': 'photo_50'}, user.token, '5.124')['response'][0]
        owner_name = owner['first_name'] + " " + owner['last_name']
        owner_photo = owner['photo_50']
    new_post = Post(user=user,
                    date_added=datetime.datetime.now(),
                    post_id=wall_data['id'],
                    owner_id=wall_data['owner_id'],
                    owner_name=owner_name,
                    owner_img_link=owner_photo,
                    from_id=wall_data['from_id'],
                    date=wall_data['date'],
                    text=wall_data['text'],
                    comments_count=wall_data.get(
                        'comments', {'count': 0})['count'],
                    likes_count=wall_data.get(
                        'likes', {'count': 0})['count'],
                    reposts_count=wall_data.get(
                        'reposts', {'count': 0})['count'],
                    views_count=wall_data.get(
                        'views', {'count': 0})['count'],
                    attachments=json.dumps(wall_data.get('attachments', [])))
    new_post.save()
    if comment is not None and len(comment) > 0:
        new_comment = Comment(user=user, comment=comment,
                              post=new_post, date=datetime.datetime.now())
        new_comment.save()
    return model_to_dict(new_post)


def send_message(message, user_id):
    community_token = 'cd4bb7c9e5628b5c7d513f91cc4bc20f0adf5bcdafcca02009f00aa092088ec7e8cabd78eb7e2959f6949'
    rand = random.randint(-32768, 32767)
    answer = vk_request('get', 'messages.send', {
                        'peer_id': user_id, 'message': message, 'random_id': rand}, community_token, '5.131')
    print(answer)
