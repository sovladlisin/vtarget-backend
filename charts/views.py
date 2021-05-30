from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
import json
from .models import Medal
# Create your views here.


@csrf_exempt
def updateMedal(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        title = data.get('title', None)
        name = data.get('name', None)
        description_gold = data.get('description_gold', None)
        description_silver = data.get('description_silver', None)
        description_copper = data.get('description_copper', None)
        description_diamond = data.get('description_diamond', None)

        if Medal.objects.filter(title=title).count() == 0:
            medal = Medal(title=title, name=name, description_gold=description_gold, description_silver=description_silver,
                          description_copper=description_copper, description_diamond=description_diamond)
            medal.save()
            return JsonResponse(model_to_dict(medal), safe=False)

        medal = Medal.objects.filter(title=title).first()
        medal.name = name
        medal.description_gold = description_gold
        medal.description_silver = description_silver
        medal.description_copper = description_copper
        medal.description_diamond = description_diamond
        medal.save()
        return JsonResponse(model_to_dict(medal), safe=False)

    return HttpResponse('Wrong request')


@csrf_exempt
def getMedals(request):
    if request.method == 'GET':
        result = []
        for medal in Medal.objects.all():
            result.append(model_to_dict(medal))
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')
