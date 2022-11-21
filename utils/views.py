from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup  # To get everything
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
import requests
import json
from django.forms.models import model_to_dict
import datetime
from .models import CollectTagsJob
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import random

IMAGE_SOURCE_URL = 'http://shutterstock.parsers.services.vtargete.ru:14292'
IMAGE_SEARCH_URL = 'http://shutterstock.parsers.services.vtargete.ru:14292/api/search'
IMAGE_TAGS_URL = 'http://shutterstock.parsers.services.vtargete.ru:14292/api/get_tags_of_image'
IMAGE_GET_URL = 'http://shutterstock.parsers.services.vtargete.ru:14292/api/get_images'

def getWord():
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # r2 = requests.get(
    #     'https://calculator888.ru/random-generator/sluchaynoye-slovo', headers=headers)
    # soup = BeautifulSoup(r2.text, features="html.parser")
    # a = soup.html.body.find('div', {"class": "blok_otvet"}).text
    job = CollectTagsJob.objects.all().first()
    dictionary = json.loads(job.data)
    index = random.randint(0, job.size - 1)
    word = dictionary[index]

    return word


def getLinks(word, word2, search, page=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    link = "https://www.shutterstock.com/ru/search/{word}+{word2}?page={page}{search}".format(
        word=word, word2=word2, page=page, search=search)
    print('shutterlink^^^:', link)
    r2 = requests.get(link, headers=headers)
    t = r2.text.split('"')
    res = {}
    for y in t:
        if 'https://www.shutterstock.com/image-photo/' in y:
            res[y] = 1

    urls = list(res.keys())
    return urls


def getSearch(word, search, times=5):
    if times == 0:
        print('empty', times)
        return [], ''
    word2 = getWord()
    links = getLinks(word, word2, search)
    if (len(links) == 0):
        return getSearch(word, search, times=times - 1)
    return links, word2


def getSearchStable(word1, word2, page, search):
    links = getLinks(word1, word2, search, page=page)
    return links


def getVtarget(word, word2, page=1):

    words = [word2.lower(), word]
    body = {'from': (int(page) - 1) * 50, 'to': int(page) * 50, 'fuilds': {
        'required_words': words, 'any_words': []}}

    r2 = requests.post(IMAGE_SEARCH_URL, data=json.dumps(body)).json()
    imgs = r2['response']['images']
    result = []
    for img in imgs:
        result.append(IMAGE_SOURCE_URL + img['url'])

    return result


def getVtargetSearch(word, times=15):
    if times == 0:
        return [], ''
    word2 = getWord()
    links = getVtarget(word, word2)
    if len(links) == 0:
        return getVtargetSearch(word, times=times - 1)
    return links, word2


def getVtargetSearchStable(word, word2, page):
    return getVtarget(word, word2, page)


@csrf_exempt
def searchShutterstock(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        word1 = data.get('word1', None)
        word2 = data.get('word2', None)
        search = data.get('search', None)
        page = data.get('page', None)

        if word2 is not None:
            return JsonResponse({'links': getSearchStable(word1, word2, search, page), 'word': word2}, safe=False)

        links, word2 = getSearch(word1, search)

        return JsonResponse({'links': links, 'word': word2}, safe=False)
    return HttpResponse('Wrong request')


@csrf_exempt
def searchVtarget(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        word1 = data.get('word1', None)
        word2 = data.get('word2', None)
        page = data.get('page', None)

        if word2 is not None:
            return JsonResponse({'links': getVtargetSearchStable(word1, word2, page), 'word': word2}, safe=False)

        links, word2 = getVtargetSearch(word1)

        return JsonResponse({'links': links, 'word': word2}, safe=False)
    return HttpResponse('Wrong request')


def getRandWord(request):
    if request.method == 'GET':
        return JsonResponse(getWord(), safe=False)
    return HttpResponse('Wrong request')


def getTagJobStatus(request):
    if request.method == 'GET':
        job = CollectTagsJob.objects.all().first()
        job.data = ''
        return JsonResponse(model_to_dict(job), safe=False)
    return HttpResponse('Wrong request')


class ResponseThen(HttpResponse):
    def __init__(self, data, then_callback, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback

    def close(self):
        super().close()
        self.then_callback()


def startCollectTagsJob(request):
    if request.method == 'GET':
        job = CollectTagsJob.objects.all().first()
        job.in_progress = True
        job.progress = '0'
        job.save()
        return ResponseThen('ok', getAllTags,  status=200)


def getAllTags(result={}, step=1, all=99999):

    def getImgTags(dict_, id):

        def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
            return not alphabet.isdisjoint(text.lower())

        new_dict = dict_
        data = {"id": id}
        r = requests.post(IMAGE_TAGS_URL, json.dumps(data)).json()
        tags = r['response']['tags']
        for tag in tags:
            if match(tag.lower()):
                new_dict[tag.lower()] = 1
        return new_dict

    start = (step - 1) * 100
    finish = step * 100

    # FINISH HERE -------------------------------------------------
    if all <= start:
        job = CollectTagsJob.objects.all().first()
        data = list(result.keys())
        job.data = json.dumps(data)
        job.in_progress = False
        job.progress = '100'
        job.last_updated = datetime.datetime.now()
        job.size = len(data)
        job.save()
        return 'Ok'

    data = {"from": start, "to": finish}
    r = requests.post(IMAGE_GET_URL, json.dumps(data)).json()
    all_count = r['response']['all_images_cnt']

    imgs = r['response']['images']
    for img in imgs:
        result = getImgTags(result, img['id'])

    # MARK PROGRESS
    job = CollectTagsJob.objects.all().first()
    job.progress = str(int(start) / int(all_count))
    job.save()

    return getAllTags(result=result, step=step + 1, all=all_count)
