from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.db import connections
import json
import pytz  # pip install pytz


def start():
    scheduler = BackgroundScheduler()
    print('start')
    scheduler.add_job(test, 'interval', minutes=20)
    scheduler.start()


def test():
    print('Performing check for posting...')
    from .models import PlannedPost, AvailableGroup
    from users.models import VkUser

    planned_posts = PlannedPost.objects.all()
    if planned_posts.count() == 0:
        closeConn()
        return 0
    for post in planned_posts:
        processPost(post)
    closeConn()


def processPost(post):
    from .models import PlannedPost, AvailableGroup
    from users.models import VkUser

    if len(post.post.user.post_token) == 0:
        print('check')
        post.delete()
        return 0

    now = datetime.now(pytz.timezone('Europe/Moscow'))
    time_now = now.hour * 100 + now.minute

    time_add = json.loads(post.time_add)
    time_add = int(time_add['hours'])*100 + int(time_add['minutes'])

    time_delete = json.loads(post.time_delete)
    time_delete = int(time_delete['hours']) * \
        100 + int(time_delete['minutes'])

    if post.on_delete is False and time_add <= time_now:
        add(post, now)
        return 0

    if post.on_delete and time_delete <= time_now:
        delete(post, now)
        return 0


def closeConn():
    for conn in connections.all():
        conn.close()


def add(post, now):
    if post.last_day_added == now.weekday():
        return 0
    if (post.every_day_marker):
        post_to_vk(post, now)
        return 0
    if now.weekday() in json.loads(post.days_add):
        post_to_vk(post, now)
    return 0


def delete(post, now):
    if post.last_day_deleted == now.weekday():
        return 0
    if (post.every_day_marker):
        remove_from_vk(post, now)
        return 0
    if now.weekday() in json.loads(post.days_delete):
        remove_from_vk(post, now)
    return 0


def getAttachments(post):
    attachments = json.loads(post.post.attachments)
    final_attachments = ''
    if len(attachments) != 0:
        for item in attachments:
            type = item['type']
            owner_id = str(item[type]['owner_id'])
            media_id = str(item[type]['id'])
            final_attachments += type+owner_id + '_' + media_id + ','
    return final_attachments


def post_to_vk(post, now):
    import random
    from think_bank.views import vk_request
    from .models import AvailableGroup
    groups = json.loads(post.target_groups_id)
    new_ids = {}
    try:
        for g_id in groups:
            target_group = AvailableGroup.objects.all().get(pk=g_id)
            rand = random.randint(-32768, 32767)
            props = {
                'owner_id': "-" + target_group.group_id,
                'from_group': post.from_group,
                'message': post.post.message,
                'attachments': getAttachments(post),
                'guid': rand,
                'mark_as_ads': post.mark_as_ads,
                'close_comments': post.close_comments,
                'mute_notifications': post.mute_notifications
            }
            posted_vk_id = ''

            posted_vk_id = vk_request('post', 'wall.post', props,
                                      post.post.user.post_token, '5.124')
            print(posted_vk_id)
            pid = posted_vk_id['response']['post_id']
            print('Post added', posted_vk_id)

            new_ids[g_id] = pid

        post.posted_vk_ids = json.dumps(new_ids)
        post.last_day_added = now.weekday()
        post.on_delete = True
        post.save()
    except:
        print('Error')
        post.delete()


def remove_from_vk(post, now):
    from think_bank.views import vk_request
    from .models import AvailableGroup
    groups = json.loads(post.target_groups_id)
    try:
        for g_id in groups:
            target_group = AvailableGroup.objects.all().get(pk=g_id)
            current_ids = json.loads(post.posted_vk_ids)
            post_id = current_ids[str(g_id)]
            props = {
                'owner_id': "-" + target_group.group_id,
                'post_id': post_id,
            }

            d = vk_request('get', 'wall.delete', props,
                           post.post.user.post_token, '5.124')
            print('Deleted', d, post_id)

        post.posted_vk_ids = json.dumps({})
        post.last_day_deleted = now.weekday()
        post.on_delete = False
        post.save()
    except:
        print('Error')
        post.delete()
