from django.db import models


class ResultItem(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    formatted_url = models.CharField(max_length=255)
    html_snippet = models.TextField()

    def __str__(self):
        return self.title


class Word(models.Model):
    text = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.text


class Query(models.Model):
    client_ip = models.CharField(max_length=15)
    search_phrase = models.CharField(max_length=255)
    total_results = models.BigIntegerField()
    result_items = models.ManyToManyField(ResultItem)
    most_common_words = models.ManyToManyField(Word)
    page_number = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'queries'

    def __str__(self):
        return self.search_phrase
