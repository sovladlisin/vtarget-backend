from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def runLegacyRequest(request):
    if request.method == 'POST':
        data_main = json.loads(request.body.decode('utf-8'))
        request_type = data_main.get('request_type', None)
        data = data_main.get('data', None)
        params = data_main.get('params', None)
        url = data_main.get('url', None)
        
        if request_type == 'POST':
            response = requests.post(url=url, data=json.dumps(data))
        if request_type == 'GET':
            response = requests.get(url=url, params=params)

        return JsonResponse(response, safe=False)
    return HttpResponse('Wrong request')