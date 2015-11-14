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
        json_obj = {}
        request_query = json.loads(request.body)

        if request_query['type'] == 'domain':
            domain_url = request_query['url']
            json_obj['url'] = domain_url
            try:
                domain_entry = TopDomain.objects.get(domain_name=domain_url)
            except TopDomain.DoesNotExist:
                return JsonResponse(json_obj)
            json_obj['isLeak'] = domain_entry.is_leak
            json_obj['accept'] = domain_entry.accept_count
            json_obj['reject'] = domain_entry.reject_count
            json_obj['pages'] = []
            if domain_entry.is_leak:
                sub_page_set = FullRequest.objects.filter(top_domain=domain_entry)
                for page_entry in sub_page_set:
                    json_obj['pages'] += [{
                        'url': page_entry.page_url,
                        'isLeak': page_entry.is_leak}]
            return JsonResponse(json_obj)

        elif request_query['type'] == 'page':
            page_url = request_query['url']
            json_obj['url'] = page_url
            try:
                page_entry = FullRequest.objects.get(page_url=page_url)
            except FullRequest.DoesNotExist:
                return JsonResponse(json_obj)
            json_obj['isLeak'] = page_entry.is_leak
            json_obj['accept'] = page_entry.accept_count
            json_obj['reject'] = page_entry.reject_count
            json_obj['leakTo'] = []
            if page_entry.is_leak:
                page_leak_to_set = LeakToURL.objects.filter(leak_from=page_entry)
                for leak_to_entry in page_leak_to_set:
                    json_obj['leakTo'] += [{
                        'url': leak_to_entry.leak_url,
                        'type': leak_to_entry.leak_type}]
            return JsonResponse(json_obj)

    return render(request, 'error.html', status=404)
