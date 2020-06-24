from django.forms import ModelForm
from default.models import Mail, Article


class MailForm(ModelForm):

    class Meta:
        model = Mail
        fields = ['name', 'subject', 'content', 'role']


class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ['name', 'title', 'subtitle', 'content']
