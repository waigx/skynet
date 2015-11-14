from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *


def test_page(request):
    return render(request, 'test_page.html')


def put(request):
    return render(request, 'error.html')


def get(request):
    if request.method == 'POST':
        request_qurey = json.loads(request.body)
        if request_qurey['type'] == 'domain':
            domain_url = request_qurey['url']
            return JsonResponse(None)
        elif request_qurey['type'] == 'page':
            page_url = request_qurey['url']
            return JsonResponse(None)

    return render(request, 'error.html')
