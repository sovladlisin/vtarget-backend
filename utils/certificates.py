from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import base64

@csrf_exempt
def runLegacyRequest(request):
    if request.method == 'POST':
        data_main = json.loads(request.body.decode('utf-8'))
        request_type = data_main.get('request_type', None)
        data = data_main.get('data', None)
        params = data_main.get('params', None)
        url = data_main.get('url', None)
        
        if request_type == 'POST':
            response = requests.post(url=url, data=json.dumps(data)).json()
        if request_type == 'GET':
            response = requests.get(url=url, params=params).json()

        return JsonResponse(response, safe=False)
    return HttpResponse('Wrong request')

def get_as_base64(url):

    return base64.b64encode(requests.get(url)).content

def runLegacyShutterstockGetImages(request):
    if request.method == 'POST':
        data_main = json.loads(request.body.decode('utf-8'))
        data = data_main.get('data', None)
        url = data_main.get('url', None)


        response = requests.post(url, data).json()
        images = response['response'].get('images', [])
        new_images = []
        for image in images:
            base = get_as_base64('http://shutterstock.parsers.services.vtargete.ru:14292' + image['url'])
            image['base'] = base
            new_images.append(image)
        all_images_cnt = response['response'].get('all_images_cnt', 0)
        
        return JsonResponse({'images': new_images, 'all_images_cnt': all_images_cnt}, safe=False)

    return HttpResponse('Wrong request')

def runLegacyShutterstock(request):
    if request.method == 'POST':
        data_main = json.loads(request.body.decode('utf-8'))
        data = data_main.get('data', None)
        url = data_main.get('url', None)
        response = requests.post(url, data).json()
        return JsonResponse(response, safe=False)
    return HttpResponse('Wrong request')