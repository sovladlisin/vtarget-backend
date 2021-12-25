from django.shortcuts import render
from .models import FutureModerator, CreatedGroup
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
import json
from users.models import VkUser
from think_bank.views import vk_request
from django.http import JsonResponse
import random
import urllib
import requests
from django.views.decorators.csrf import csrf_exempt
# from think_bank.views import send_message
# Create your views here.


@csrf_exempt
def copyRequest(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        group_url = data.get('group_url', None)
        user_pk = data.get('user_pk', None)
        user = VkUser.objects.get(pk=user_pk)
        url = copy_group(group_url, user.post_token)

        return JsonResponse({'group_url': url}, safe=False)

    return HttpResponse('Wrong request')


@csrf_exempt
def copy_group(id, post_token):
    def assign(dics, key, value):
        if value is None:
            return dics
        dics[key] = value
        return dics

    def send_message(role, user_id, group_url, token, group_id):
        message = 'Здравствуйте, была созданна новая группа, в которой вам нужно получить управляющую должность ' + \
            str(role) + '. Пожалуйста, вступите в группу по ссылке: ' + str(group_url)
        rand = random.randint(-32768, 32767)
        answer = vk_request('post', 'messages.send', {
                            'peer_id': int(user_id), 'message': message, 'random_id ': rand, 'group_id': int(group_id)}, token, '5.45')

    def getAttachments(post):
        attachments = post['attachments']
        final_attachments = ''
        if len(attachments) != 0:
            for item in attachments:
                type = item['type']
                print(item)
                if type == 'link':
                    link_url = item[type]['url']
                    # photo_id = item[type]['photo']['id']
                    # photo_owner = item[type]['photo']['owner_id']
                    # final_attachments += 'photo' + \
                    #     str(photo_owner) + '_' + \
                    #     str(photo_id) + ',' + str(link_url)
                    final_attachments += link_url
                else:
                    owner_id = str(item[type]['owner_id'])
                    media_id = str(item[type]['id'])
                    final_attachments += type+owner_id + '_' + media_id + ','
        return final_attachments

    def handle_contacts(contacts, og_group_id, g_id, token, created_group, created_group_url):

        cont = []
        for i in contacts:
            cont.append(i['user_id'])

        managers = vk_request('get', 'groups.getMembers', {
                              'group_id': og_group_id, 'filter': 'managers'}, token, '5.126')
        for m in managers['response']['items']:
            contact_flag = 1 if m['id'] in cont else 0
            moderators_count = 0
            if m['role'] != 'creator':
                new_future_moderator = FutureModerator(
                    role=m['role'], is_contact=contact_flag, vk_id=m['id'], group_id=g_id)
                new_future_moderator.save()
                moderators_count += 1
                # send_message(m['role'], m['id'],
                #              created_group_url, message_token, g_id)
                # r = vk_request('get', 'groups.editManager', {
                #                'group_id': g_id, 'user_id': m['id'], 'role': m['role'], 'is_contact': contact_flag}, token, '5.126')
        created_group.number_of_moderators = moderators_count
        created_group.save()

    def handle_posts(og_group, new_group, token):
        posts = []
        wall = vk_request('get', 'wall.get', {
                          'owner_id': og_group * -1, 'count': 100}, token, '5.126')['response']['items']
        for post in reversed(wall):
            close_comments = post['comments']['can_post'] * -1
            attachments = getAttachments(post)
            text = post['text']
            rand = random.randint(-32768, 32767)
            props = {
                'owner_id': "-" + str(new_group),
                'from_group': 1,
                'message': text,
                'attachments': attachments,
                'guid': rand,
                'close_comments': close_comments,
                'mute_notifications': 1
            }
            posted_vk_id = vk_request(
                'post', 'wall.post', props, token, '5.124')

    def handle_create(title, desc, g_type, public_cat, public_subcategory, subtype, token):
        created_group_info = vk_request('get', 'groups.create', {
            'title': title,
            'description': desc,
            'type': 'public' if g_type == 'page' else g_type,
            'public_category': public_cat,
            'public_subcategory': public_subcategory,
            'subtype': subtype
        },
            token, '5.126')
        
        print(created_group_info)
        return created_group_info['response']['id']

    def handle_edit(g_id, access, desc, website, subject, phone, public_cat, public_sub_cat, country, city, age_limits, addresses, token):
        settings = vk_request('get', 'groups.setSettings', {
                              'messages': 1, 'group_id': int(g_id)}, token, '5.126')

        props = {}
        assign(props, 'description', desc)
        assign(props, 'website', website)
        assign(props, 'group_id', g_id)
        assign(props, 'access', access)
        assign(props, 'subject', subject)
        assign(props, 'phone', phone)
        assign(props, 'public_category', public_cat)
        assign(props, 'public_subcategory', public_sub_cat)
        assign(props, 'country', country)
        assign(props, 'city', city)
        assign(props, 'age_limits', age_limits)
        assign(props, 'addresses', addresses)

        edit = vk_request('get', 'groups.edit', props, token, '5.126')

        return 1

    def handle_photos(created_group_id, g_cover, g_photo, token):
        photo_url = vk_request('get', 'photos.getOwnerPhotoUploadServer', {
                               'owner_id': created_group_id * -1}, token, '5.126')
        photo_url = photo_url['response']['upload_url']

        cover_url = vk_request('get', 'photos.getOwnerCoverPhotoUploadServer', {
                               'group_id': created_group_id, 'crop_y2': g_cover['images'][-1]['height'], 'crop_x2': g_cover['images'][-1]['width']}, token, '5.126')
        cover_url = cover_url['response']['upload_url']

        urllib.request.urlretrieve(g_photo, "logo.png")
        photo_server = requests.post(
            photo_url, files={'photo': open("logo.png", 'rb')}).json()

        urllib.request.urlretrieve(g_cover['images'][-1]['url'], "cover.png")
        photo_cover = requests.post(
            cover_url, files={'photo': open("cover.png", 'rb')}).json()

        photo_answer = vk_request('post', 'photos.saveOwnerPhoto', {
                                  'server': photo_server['server'], 'hash': photo_server['hash'], 'photo': photo_server['photo']}, token, '5.126')
        cover_answer = vk_request('post', 'photos.saveOwnerCoverPhoto', {
                                  'hash': photo_cover['hash'], 'photo': photo_cover['photo']}, token, '5.126')
        return 1

    def handle_address(og_group, new_group, token):
        addresses = []
        r_addresses = vk_request('get', 'groups.getAddresses', {
                                 'group_id': og_group}, token, '5.126')
        for a in r_addresses['response']['items']:
            a['group_id'] = new_group
            add_r = vk_request('get', 'groups.addAddress',
                               a, token, '5.126')

    def handle_code(created_group, token):
        code = vk_request('get', 'groups.getCallbackConfirmationCode', {
            'group_id': created_group.group_id}, token, '5.126')['response']['code']
        # print(code)
        created_group.code = code
        created_group.save()

    def handle_callback_server(created_group, token):
        server_id = vk_request('get', 'groups.addCallbackServer', {
            'group_id': created_group.group_id, 'url': 'https://vtarget-backend.herokuapp.com/bot-moderators', 'title': 'Managers'}, token, '5.126')['response']['server_id']
        # print(server_id)
        d = vk_request('get', 'groups.setCallbackSettings', {
            'group_id': created_group.group_id, 'server_id': server_id, 'group_join': 1}, token, '5.126')
        # print(d)

    # CODE ----------------------------------------------------------------------------
    #
    #
    # CODE ----------------------------------------------------------------------------

    group_id = id

    group = vk_request('get', 'groups.getById', {
                       'group_id': group_id, 'fields': 'activity,addresses,city,contacts,country,cover,crop_photo,screen_name,type'}, post_token, '5.126')
    print(group)
    group = group['response'][0]
    g_screen_name = group['screen_name']
    group_id = group['id']
    g_activity = group.get('activity', None)
    g_contacts = group.get('contacts', None)
    g_addresses = group.get('addresses', None)

    g_city = group.get('city', None)
    if g_city is not None:
        g_city = g_city['id']

    g_country = group.get('country', None)
    if g_country is not None:
        g_country = g_country['id']

    g_cover = group.get('cover', None)

    g_type = group.get('type', None)
    g_photo = group['photo_200']

    current_setting = vk_request('get', 'groups.getSettings', {
        'group_id': group_id}, post_token, '5.126')
    print(current_setting)

    current_setting = current_setting['response'] 

    g_title = current_setting.get('title', None)
    g_website = current_setting.get('website', None)
    g_public_category = current_setting.get('public_category', None)
    g_description = current_setting.get('description', None)
    g_phone = current_setting.get('phone', None)
    g_public_subcategory = current_setting.get('public_subcategory', None)
    g_age_limits = current_setting.get('age_limits', None)

    # posts = []
    # wall = vk_request('get', 'wall.get', {
    #                   'owner_id': group_id * -1, 'count': 100}, post_token, '5.126')['response']['items']
    # for post in wall:
    #     close_comments = post['comments']['can_post'] * -1
    #     attachments = getAttachments(post)
    #     text = post['text']
    #     posts.append({'text': text, 'attachments': attachments,
    #                   'close_comments': close_comments})

    created_group_id = handle_create(
        g_title, g_description, g_type, g_public_category, g_public_subcategory, 2, post_token)

    url_type = 'public' if g_type == 'page' else g_type
    created_group_url = 'https://vk.com/' + \
        str(url_type) + str(created_group_id)
    created_group = CreatedGroup(
        group_id=created_group_id, number_of_moderators=0)

    subject = 8  # настраиваемое поле
    access = 0  # настраиваемое поле

    try:
        edit_result = handle_edit(created_group_id, access, g_description, g_website, subject, g_phone, g_public_category,
                                  g_public_subcategory, g_country, g_city, g_age_limits, group['addresses']['is_enabled'], post_token)
    except:
        pass

    try:
        photo_result = handle_photos(
            created_group_id, g_cover, g_photo, post_token)
    except:
        pass

    try:
        handle_address(group_id, created_group_id, post_token)
    except:
        pass

    try:
        handle_posts(group_id, created_group_id, post_token)
    except:
        pass

    try:
        handle_contacts(g_contacts, group_id, created_group_id,
                        post_token, created_group, created_group_url)
    except:
        pass

    handle_code(created_group, post_token)
    handle_callback_server(created_group, post_token)

    return created_group_url
