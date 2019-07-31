from django.test import TestCase
from django.urls import reverse
from django.utils.safestring import SafeText


class TestHome(TestCase):
    def test_anonumous(self):
        response = self.client.get(reverse('home'))
        assert response.status_code == 200, 'Should be callable by anyone'


class TestSearchResult(TestCase):
    def test_without_query(self):
        response = self.client.get(reverse('search_result'))
        assert response.status_code == 302, 'Should be redirected'
        assert response.url == '/', 'Should be redirected to home page'

    def test_with_query(self):
        search_result_url = reverse('search_result')

        query = 'cat'
        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.status_code == 200, 'Should access a page'

        # same query second time (getting from db):
        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.status_code == 200, 'Should access a page'

        # spaces in query
        query = '++++'
        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.status_code == 302, 'Should be redirected'
        assert response.url == '/', 'Should be redirected to home page'

        # no results query
        query = 'dklfjdsiffsdfvmkeom'
        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.status_code == 200, 'Should access page with no results'

        # links only query
        query = 'dog:link'
        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.status_code == 200, 'Should access a page'

        # same query second time (getting from db):
        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.status_code == 200, 'Should access a page'

    def test_page_number(self):
        search_result_url = reverse('search_result')
        query = 'cat'

        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.context['page_no'] == 1, 'Should show 1st page'

        page = 7
        response = self.client.get(f'{search_result_url}?query={query}&page={page}')
        assert response.context['page_no'] == 7, 'Should show 7th page'

        page = 14
        response = self.client.get(f'{search_result_url}?query={query}&page={page}')
        assert response.context['page_no'] == 10, 'Should show 10th page'

        page = 0
        response = self.client.get(f'{search_result_url}?query={query}&page={page}')
        assert response.context['page_no'] == 1, 'Should show 1st page'

        page = -15
        response = self.client.get(f'{search_result_url}?query={query}&page={page}')
        assert response.context['page_no'] == 1, 'Should show 1st page'

        page = 'abcd'
        response = self.client.get(f'{search_result_url}?query={query}&page={page}')
        assert response.context['page_no'] == 1, 'Should show 1st page'

    def test_common_words(self):
        search_result_url = reverse('search_result')

        query = 'cat'
        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.context['most_common_words'] is not None, 'Should return common words'
        assert type(response.context['most_common_words']) == list, 'Common words should be a list'

        # no common words with ':link' parameter
        query = 'cat:link'
        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.context['most_common_words'] is None, 'Should return no common words'

    def test_links_only(self):
        search_result_url = reverse('search_result')

        query = 'cat'
        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.context['links_only'] is False, 'Should return False'

        query = 'cat:link'
        response = self.client.get(f'{search_result_url}?query={query}')
        assert response.context['links_only'] is True, 'Should return True'

    def test_items(self):
        search_result_url = reverse('search_result')

        query = 'cat'
        response = self.client.get(f'{search_result_url}?query={query}')
        for item in response.context['items']:
            assert type(item['title']) == str, 'Should be string'
            assert type(item['link']) == str, 'Should be string'
            assert type(item['formatted_url']) == str, 'Should be string'
            assert type(item['html_snippet']) == SafeText, 'Should be SafeText'

        query = 'cat:link'
        response = self.client.get(f'{search_result_url}?query={query}')
        for item in response.context['items']:
            assert type(item['link']) == str, 'Should be string'


class TestSettings(TestCase):
    def test_get(self):
        response = self.client.get(reverse('settings'))
        assert response.status_code == 200, 'Should access settings page'

    def test_post(self):
        data = {
            'days': 2,
            'hours': 14,
            'minutes': 37,
        }
        response = self.client.post(reverse('settings'), data)
        assert response.status_code == 200, 'Should access settings page'
        assert self.client.session.get('time_limit') == 3757, 'Time limit should be changed'
