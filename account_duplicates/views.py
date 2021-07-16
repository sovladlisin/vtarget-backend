from django.http import JsonResponse
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from users.models import VkUser
from think_bank.views import vk_request
import requests
import json
from PIL import Image
import imagehash
from .models import AccountDuplicateJob
# Create your views here.
import datetime
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt


class ResponseThen(HttpResponse):
    def __init__(self, data, then_callback, job, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback
        self.job = job

    def close(self):
        super().close()
        self.then_callback(self.job)


@csrf_exempt
def startAnalysis(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)
        user = VkUser.objects.get(pk=user_id)

        job = None
        jobs = AccountDuplicateJob.objects.all().filter(owner__pk=user.pk)
        if jobs.count() == 0:
            job = AccountDuplicateJob(
                data='[]', owner=user, in_progress=True, progress='0')
        else:
            job = jobs.first()

        job.last_updated = datetime.datetime.now()
        job.save()
        return ResponseThen('ok', search_people, job, status=200)


@csrf_exempt
def getUserJob(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)
        user = VkUser.objects.get(pk=user_id)

        jobs = AccountDuplicateJob.objects.all().filter(owner__pk=user.pk)
        if jobs.count() == 0:
            job = AccountDuplicateJob(
                data='[]', owner=user, in_progress=False, progress='0')
        else:
            job = jobs.first()
        result = model_to_dict(job)
        result['data'] = json.loads(result['data'])

        return JsonResponse(result, safe=False)


def search_people(job):
    user_id = job.owner.user_id
    token = job.owner.token

    def compare_images(img_link1, img_link2):

        hash0 = imagehash.average_hash(Image.open(
            requests.get(img_link1, stream=True).raw))
        hash1 = imagehash.average_hash(Image.open(
            requests.get(img_link2, stream=True).raw))
        cutoff = 5  # maximum bits that could be different between the hashes.

        if hash0 - hash1 < cutoff:
            return True
        else:
            return False

    def compare(o, o2):

        if o['has_photo'] != o2['has_photo']:
            return False

        index = 0

        index = index + \
            1 if o.get('sex', None) == o2.get('sex', None) else index
        index = index + \
            10 if o.get('bdate', None) == o2.get('bdate', None) else index
        index = index + 3 if o.get('country',
                                   None) == o2.get('country', None) else index
        index = index + 1 if o.get('timezone',
                                   None) == o2.get('timezone', None) else index
        index = index + \
            1 if o.get('about', None) == o2.get('about', None) else index
        index = index + \
            1 if o.get('activities', None) == o2.get(
                'activities', None) else index
        index = index + \
            1 if o.get('books', None) == o2.get('books', None) else index
        index = index + \
            10 if o.get('career', None) == o2.get('career', None)else index
        index = index + 1 if o.get('faculty',
                                   None) == o2.get('faculty', None) else index
        index = index + \
            1 if o.get('faculty_name', None) == o2.get(
                'faculty_name', None) else index
        index = index + \
            1 if o.get('graduation', None) == o2.get(
                'graduation', None) else index
        index = index + \
            1 if o.get('home_phone', None) == o2.get(
                'home_phone', None) else index
        index = index + 1 if o.get('home_town',
                                   None) == o2.get('home_town', None) else index
        index = index + \
            10 if o.get('interests', None) == o2.get(
                'interests', None) else index
        index = index + 1 if o.get('military',
                                   None) == o2.get('military', None) else index
        index = index + 1 if o.get('nickname',
                                   None) == o2.get('nickname', None) else index
        index = index + \
            1 if o.get('occupation', None) == o2.get(
                'occupation', None) else index
        index = index + 1 if o.get('personal',
                                   None) == o2.get('personal', None) else index
        index = index + \
            10 if o.get('quotes', None) == o2.get('quotes', None) else index
        index = index + 1 if o.get('relation',
                                   None) == o2.get('relation', None) else index
        index = index + 1 if o.get('relatives',
                                   None) == o2.get('relatives', None) else index
        index = index + 1 if o.get('schools',
                                   None) == o2.get('schools', None) else index
        index = index + \
            1 if o.get('site', None) == o2.get('site', None) else index
        index = index + 40 if o.get('status', None) == o2.get(
            'status', None) and o.get('status', None) != '' else index
        index = index + \
            1 if o.get('universities', None) == o2.get(
                'universities', None) else index
        index = index + \
            1 if o.get('university', None) == o2.get(
                'university', None) else index
        index = index + \
            1 if o.get('university_name', None) == o2.get(
                'university_name', None) else index

        # 31
        if index > 20:
            return compare_images(o['photo_max'], o2['photo_max'])
        return False

    fields = ' photo_id, sex, bdate, city, country, home_town, has_photo, photo_max, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, timezone, screen_name, maiden_name, crop_photo, career, military, blacklisted, blacklisted_by_me'
    current_user_params = {'user_ids': [user_id], 'fields': fields}
    current_user_response = vk_request(
        'post', 'users.get', current_user_params, token, '5.131')
    current_user_obj = current_user_response['response'][0]

    search_params = {'q': current_user_obj['first_name'] + ' ' +
                     current_user_obj['last_name'], 'fields': fields, 'sort': 0, 'count': 1000}
    search_response = vk_request(
        'post', 'users.search', search_params, token,  '5.131')
    search_list = search_response['response']['items']

    result = []
    count = search_response['response']['count']
    i = 0

    for item in search_list:
        i += 1
        if compare(current_user_obj, item):
            result.append(item)
        if i % 10 == 0:
            print(count)
            job.progress = str(int(i) / int(count))
            job.save()

    job.progress = '1'
    job.in_progress = False
    job.data = json.dumps(result)
    job.save()
