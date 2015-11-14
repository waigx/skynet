
def to_top_domain(raw_url):
    if (raw_url.find('http://') == 0) or (raw_url.find('https://') == 0):
        has_header = True
    else:
        has_header = False
    domain_url = raw_url.split('/')[2 if has_header else 0]
    domain_url = '.'.join(domain_url.split('.')[-2:])
    return domain_url
