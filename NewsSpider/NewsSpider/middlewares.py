import random


class RandomUa(object):
    def process_request(self, spider, request):
        ua = random.choice(spider.settings.get('USER_AGENTS'))
        request.headers['User-Agent'] = ua
