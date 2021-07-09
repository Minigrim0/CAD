from django.contrib import admin

from default.models import Article, Mail, Message, MailingList

ARTICLE_DISPLAY_SIZE = 75


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "content_preview")
    list_filter = ("name", "date")
    date_hierachy = "date"
    ordering = ("date",)
    search_fields = ("title", "subtitle", "content")

    fields = ("name", "title", "subtitle", "content")

    @staticmethod
    def content_preview(article: Article) -> str:
        """Renders a short version of the article

        Args:
            article (Article): The article to render a shortened version of

        Returns:
            str: The shortened version of the article
        """
        text = article.title[0:ARTICLE_DISPLAY_SIZE]
        if len(article.title) > ARTICLE_DISPLAY_SIZE:
            return text + "..."
        return text

    content_preview.short_description = u"Titre de la section"


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subject", "role")
    list_filter = ("id", "name", "subject", "role")
    ordering = ("-id",)
    search_fields = ("name", "subject", "id")

    fields = (("name", "subject"), ("content"), "role")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "contact_mail", "seen")
    list_filter = ("id", "subject", "contact_mail", "seen")
    ordering = ("-id",)
    search_fields = ("subject", "subject", "id")

    fields = (
        ("subject", "content"),
        ("contact_mail", "seen"),
    )


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_filter = (
        "id",
        "name",
    )
    ordering = ("-id",)
    search_fields = ("name",)

    fields = (
        "name",
        "users",
    )
