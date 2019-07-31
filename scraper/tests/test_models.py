import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestResultItem:
    def test_model(self):
        obj = mixer.blend('scraper.ResultItem')
        assert obj.pk == 1, 'Should create a Result Item'

    def test_str(self):
        obj = mixer.blend('scraper.ResultItem', title='Item 1')
        result = obj.__str__()
        assert result == 'Item 1', 'Should return item title'


class TestWord:
    def test_model(self):
        obj = mixer.blend('scraper.Word')
        assert obj.pk == 1, 'Should create a Word'

    def test_str(self):
        obj = mixer.blend('scraper.Word', text='Word 1')
        result = obj.__str__()
        assert result == 'Word 1', 'Should return word text'


class TestQuery:
    def test_model(self):
        obj = mixer.blend('scraper.Query')
        assert obj.pk == 1, 'Should create a Query'

    def test_str(self):
        obj = mixer.blend('scraper.Query', search_phrase='cat')
        result = obj.__str__()
        assert result == 'cat', 'Should return query search phrase'
