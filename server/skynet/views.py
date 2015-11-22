from django.shortcuts import render
import json
from django.http import JsonResponse
from utils.toTopDomain import to_top_domain
from .models import *


def test_page(request):
    return render(request, 'demo/index.html')


def view_main(request):
    domain_set = TopDomain.objects.all()
    for item in domain_set:
        item.accept_rate = str(item.accept_count/(item.accept_count+item.reject_count) * 100)+'%'
    return render(request, 'terminator_view_main.html', {'domain': domain_set})


def view_domain(request):
    domain_url = request.path[10:]
    print domain_url
    try:
        domain_entry = TopDomain.objects.get(domain_name=domain_url)
    except TopDomain.DoesNotExist:
        return render(request, 'error.html')
    sub_page_set = FullRequest.objects.filter(top_domain=domain_entry)
    for item in sub_page_set:
        item.accept_rate = str(item.accept_count/(item.accept_count+item.reject_count) * 100)+'%'
    return render(request, 'terminator_view_domain.html', {'pages': sub_page_set,
                                                           'top_domain': to_top_domain(domain_url)})


def view_full_request(request):
    page_url = request.path[8:]
    try:
        page_entry = FullRequest.objects.get(page_url=page_url)
    except FullRequest.DoesNotExist:
        return render(request, 'error.html')
    if page_entry.is_leak:
        page_leak_to_set = LeakToURL.objects.filter(leak_from=page_entry)
    return render(request, 'terminator_view_request.html', {'pages': page_leak_to_set,
                                                            'page_url': page_url})





def demo_page(request):
    return render(request, 'demo/index.html')


def api_get_page(request):
    return render(request, 'demo/get.html')


def api_put_page(request):
    return render(request, 'demo/put.html')


def put(request):
    if request.method == 'POST':
        json_obj = {'isSuccess': False}
        put_request = json.loads(request.body)

        # process json request
        if ('url' not in put_request) or ('isLeak' not in put_request):
            return JsonResponse(json_obj)
        if (put_request['isLeak'] == True) \
                and (('leakTo' not in put_request) or ('isAccept' not in put_request)):
            return JsonResponse(json_obj)
        raw_url = put_request['url']
        is_leak = put_request['isLeak']
        is_accept = True if 'isAccept' not in put_request else put_request['isAccept']
        leak_to_sets = put_request['leakTo'] if is_leak else []
        domain_url = to_top_domain(raw_url)

        # process top domain table
        try:
            domain_entry = TopDomain.objects.get(domain_name=domain_url)
        except TopDomain.DoesNotExist:
            domain_entry = TopDomain.objects.create()
            domain_entry.domain_name = domain_url
            domain_entry.accept_count = 0
            domain_entry.reject_count = 0
            domain_entry.is_leak = False
        domain_entry.accept_count += 1 if is_accept else 0
        domain_entry.reject_count += 0 if is_accept else 1
        domain_entry.is_leak = domain_entry.is_leak or is_leak
        domain_entry.save()

        # process full request url table
        try:
            page_entry = FullRequest.objects.get(page_url=raw_url)
        except FullRequest.DoesNotExist:
            page_entry = FullRequest.objects.create()
            page_entry.page_url = raw_url
            page_entry.is_leak = False
            page_entry.accept_count = 0
            page_entry.reject_count = 0
            page_entry.top_domain = domain_entry
        page_entry.accept_count += 1 if is_accept else 0
        page_entry.reject_count += 0 if is_accept else 1
        page_entry.is_leak = domain_entry.is_leak or is_leak
        page_entry.save()

        # process leak to url table
        for leak_to_obj in leak_to_sets:
            if ('url' not in leak_to_obj) or ('type' not in leak_to_obj):
                return JsonResponse(json_obj)
            leak_to_entry = LeakToURL.objects.create()
            leak_to_entry.leak_url = leak_to_obj['url']
            leak_to_entry.leak_type = leak_to_obj['type']
            leak_to_entry.leak_from = page_entry
            leak_to_entry.save()
        json_obj['isSuccess'] = True
        return JsonResponse(json_obj)

    return render(request, 'error.html', status=404)


def get(request):
    if request.method == 'POST':
        json_obj = {}
        request_query = json.loads(request.body)

        if request_query['type'] == 'domain':
            raw_url = request_query['url']
            domain_url = to_top_domain(raw_url)
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
