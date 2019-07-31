from datetime import timedelta, datetime

from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.safestring import mark_safe

from googlescraper.settings import TIME_LIMIT_DEFAULT
from scraper.decorators import check_server_connection
from scraper.models import ResultItem, Word, Query
from scraper.utils import (google_search, get_most_common_words, get_client_ip,
                           get_page)


def home(request):
    return render(request, 'scraper/home.html')


@check_server_connection
def search_result(request):
    query = request.GET.get('query')
    if query is None or query.strip() == '':
        return redirect('home')

    client_ip = get_client_ip(request)
    page = get_page(request.GET.get('page', 1))
    query = query.strip()
    links_only = query[-5:] == ':link' and len(query) > 5
    if links_only:
        query = query[:-5]

    # check if getting resuts from db is possible
    time_limit = request.session.get('time_limit', TIME_LIMIT_DEFAULT)
    time_limit_delta = timezone.now() - timedelta(minutes=time_limit)

    search_result_query = Query.objects.filter(
        timestamp__gte=time_limit_delta,
        client_ip=client_ip,
        search_phrase=query.lower(),
        page_number=page
    )

    # get results from db
    if search_result_query.exists():
        q = search_result_query.last()
        total_results = q.total_results
        if links_only:
            items = [{
                'link': item.link,
            } for item in q.result_items.all()]
            most_common_words = None
        else:
            items = [{
                'title': item.title,
                'link': item.link,
                'formatted_url': item.formatted_url,
                'html_snippet': mark_safe(item.html_snippet)
            } for item in q.result_items.all()]
            most_common_words = q.most_common_words.all()

    # download results from google api
    else:
        start_index = 1 if page == 1 else page * 10 - 9
        response = google_search(search_query=query, start_index=start_index)

        # check if there are results
        try:
            response['items']
        except KeyError:
            return render(request, 'scraper/no_results.html')

        # save search result to db
        q = Query.objects.create(
            client_ip=client_ip,
            search_phrase=query.lower(),
            total_results=response['searchInformation']['totalResults'],
            page_number=page
        )
        for item in response['items']:
            result_item, created = ResultItem.objects.get_or_create(
                title=item['title'],
                link=item['link'],
                formatted_url=item['formattedUrl'],
                html_snippet=item['htmlSnippet'])
            q.result_items.add(result_item)

        # get 10 most common words from page
        all_words = ''
        for item in response['items']:
            all_words += item['title'].lower() + item['snippet'].lower()
        most_common_words = get_most_common_words(all_words, 10)

        for word in most_common_words:
            common_word, created = Word.objects.get_or_create(text=word)
            q.most_common_words.add(common_word)
        q.save()

        total_results = response['searchInformation']['totalResults']

        if links_only:
            items = [{
                'link': item['link'],
            } for item in response['items']]
            most_common_words = None
        else:
            items = [{
                'title': item['title'],
                'link': item['link'],
                'formatted_url': item['formattedUrl'],
                'html_snippet': mark_safe(item['htmlSnippet'])
            } for item in response['items']]

    ctx = {
        'total_results': total_results,
        'items': items,
        'most_common_words': most_common_words,
        'page_no': page,
        'previous_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < 10 else None,
        'links_only': links_only,
    }
    return render(request, 'scraper/search_result.html', ctx)


def settings(request):
    if request.method == 'POST':
        days = int(request.POST.get('days', 0))
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', TIME_LIMIT_DEFAULT))
        request.session['time_limit'] = days * 1440 + hours * 60 + minutes
    else:
        time_limit = request.session.get('time_limit', TIME_LIMIT_DEFAULT)
        d = datetime(1, 1, 1) + timedelta(minutes=time_limit)
        days = d.day - 1
        hours = d.hour
        minutes = d.minute

    ctx = {
        'days': days,
        'hours': hours,
        'minutes': minutes
    }
    return render(request, 'scraper/settings.html', ctx)
