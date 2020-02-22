from django.forms import ModelForm
from default.models import Mail


class MailForm(ModelForm):

    class Meta:
        model = Mail
        fields = ['name', 'subject', 'content', 'role']
