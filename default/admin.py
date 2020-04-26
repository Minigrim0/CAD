from django.contrib import admin
from default.models import Article, Mail, Message

ARTICLE_DISPLAY_SIZE = 75


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'content_preview')
    list_filter = ('name', 'date')
    date_hierachy = 'date'
    ordering = ('date', )
    search_fields = ('title', 'subTitle', 'content')

    fields = ('name', 'title', 'subTitle', 'content')

    def content_preview(self, article):
        text = article.title[0:ARTICLE_DISPLAY_SIZE]
        if len(article.title) > ARTICLE_DISPLAY_SIZE:
            return text + "..."
        else:
            return text

    content_preview.short_description = u'Titre de la section'


class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject')
    list_filter = ('id', 'name', 'subject')
    ordering = ('-id', )
    search_fields = ('name', 'subject', 'id')

    fields = (
        ('name', 'subject'),
        ('content'),
    )


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'contact_mail')
    list_filter = ('id', 'subject', 'contact_mail')
    ordering = ('-id', )
    search_fields = ('subject', 'subject', 'id')

    fields = (
        ('subject', 'contact_mail'),
        ('content'),
    )


admin.site.register(Article, ArticleAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(Message, MessageAdmin)
