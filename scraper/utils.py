from collections import Counter
from string import punctuation

from googleapiclient.discovery import build
from googlescraper.settings import GOOGLE_API_KEY, GOOGLE_CSE_ID


def google_search(search_query, start_index, **kwargs):
    service = build('customsearch', 'v1', developerKey=GOOGLE_API_KEY)
    response = service.cse().list(q=search_query, gl='pl', cx=GOOGLE_CSE_ID,
                                  start=start_index, **kwargs).execute()
    return response


def get_most_common_words(words, count):
    table = str.maketrans(punctuation + '·' + '–', (len(punctuation) + 2) * ' ')
    c = Counter(words.translate(table).split())
    return [w[0] for w in c.most_common(count)]


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_page(p):
    try:
        page = int(p)
        if page > 10:
            return 10
        if page < 1:
            return 1
        return page
    except ValueError:
        return 1
