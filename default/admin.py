from django.contrib import admin
from default.models import Article

ARTICLE_DISPLAY_SIZE = 75

class ArticleAdmin(admin.ModelAdmin):
    list_display  = ('name', 'date', 'content_preview')
    list_filter   = ('name', 'date')
    date_hierachy = 'date'
    ordering      = ('date', )
    search_fields = ('title', 'subTitle', 'content')

    fields = ('title', 'subTitle', 'content')

    def content_preview(self, article):
        text = article.title[0:ARTICLE_DISPLAY_SIZE]
        if len(article.title) > ARTICLE_DISPLAY_SIZE:
            return text + "..."
        else:
            return text

    content_preview.short_description = u'Titre de la section'

admin.site.register(Article, ArticleAdmin)
