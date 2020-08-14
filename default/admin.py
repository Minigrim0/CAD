from django.contrib import admin

from default.models import Article, Mail, Message, MailingList

ARTICLE_DISPLAY_SIZE = 75


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'content_preview')
    list_filter = ('name', 'date')
    date_hierachy = 'date'
    ordering = ('date', )
    search_fields = ('title', 'subtitle', 'content')

    fields = ('name', 'title', 'subtitle', 'content')

    def content_preview(self, article):
        text = article.title[0:ARTICLE_DISPLAY_SIZE]
        if len(article.title) > ARTICLE_DISPLAY_SIZE:
            return text + "..."
        else:
            return text

    content_preview.short_description = u'Titre de la section'


class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject', 'role')
    list_filter = ('id', 'name', 'subject', 'role')
    ordering = ('-id', )
    search_fields = ('name', 'subject', 'id')

    fields = (
        ('name', 'subject'),
        ('content'),
        'role'
    )


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'contact_mail', 'seen')
    list_filter = ('id', 'subject', 'contact_mail', 'seen')
    ordering = ('-id', )
    search_fields = ('subject', 'subject', 'id')

    fields = (
        ('subject', 'content'),
        ('contact_mail', 'seen'),
    )


class MailingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('id', 'name',)
    ordering = ('-id', )
    search_fields = ('name',)

    fields = (
        'name',
        'users',
    )


admin.site.register(Article, ArticleAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MailingList, MailingListAdmin)
