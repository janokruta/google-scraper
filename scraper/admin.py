from django.contrib import admin

from scraper.models import Query, ResultItem, Word


class QueryAdmin(admin.ModelAdmin):
    list_display = ['search_phrase', 'page_number', 'client_ip', 'timestamp']


class ResultItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'link']


class WordAdmin(admin.ModelAdmin):
    list_display = ['text']


admin.site.register(Query, QueryAdmin)
admin.site.register(ResultItem, ResultItemAdmin)
admin.site.register(Word, WordAdmin)
