import logging

from django.db import models
from django.shortcuts import reverse
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from cad.settings import EMAIL_HOST_USER, SITE_DOMAIN, DEBUG


class Article(models.Model):
    """The article model"""

    name = models.CharField(max_length=100, default="Article", verbose_name="Nom de l'article")
    title = models.TextField(null=True)
    subtitle = models.TextField(null=True)
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de modification")

    def __str__(self):
        return self.name


class Mail(models.Model):
    """The Mail model"""

    name = models.CharField(max_length=150, default="Mail template", verbose_name="Nom du template")
    subject = models.CharField(max_length=150, default="CAD - Cours à domicile", verbose_name="Sujet")
    content = models.TextField(default="None", verbose_name="Contenu")

    choices = (
        ("a", "verification de l'adresse mail (coach et élèvre)"),
        ("b", "mail de bienvenue (élève)"),
        ("c", "proposition desinscription (élève)"),
        ("d", "solde dangereux (élève)"),
        ("e", "proposition de mission (coach)"),
        ("f", "attribution de mission (coach)"),
        ("g", "mission attribuée à un autre coach (coach)"),
        ("h", "Template non automatique"),
        ("i", "Message envoyé"),
        ("j", "Votre planning de cours (élève)"),
    )

    role = models.CharField(max_length=1, choices=choices, verbose_name="Role du mail")
    to = models.ForeignKey(User, null=True, verbose_name="Envoyé à", on_delete=models.CASCADE)

    def _sendAsNotif(self, user, title, content):
        from users.models import Notification

        Notification.objects.create(
            user=user,
            author="L'équipe CAD",
            title=title,
            content=content
        )

    def formatted_content(self, user: User, student: User = None, final_schedule: str = None, request=None) -> str:
        """Formats the content of the mail using the pre-defined tags

        Args:
            user (User): The user this mail is addressed to

        Returns:
            str: The formatted mail content
        """
        content = str(self.content)
        content = content.replace("<LASTNAME>", str(user.last_name))
        content = content.replace("<FIRSTNAME>", str(user.first_name))
        content = content.replace("<BIRTHDATE>", str(user.profile.birthDate))
        content = content.replace("<COURSES>", str(user.profile.courses))
        content = content.replace("<SCHOOLLEVEL>", str(user.profile.birthDate))
        content = content.replace("<SECRETKEY>", str(user.profile.secret_key))

        if student is not None:
            content = content.replace("<STUDENT_FIRST_NAME>", str(student.first_name))
            content = content.replace("<STUDENT_LAST_NAME>", str(student.first_name))
        if final_schedule is not None:
            content = content.replace("<REQUEST_SCHEDULE>", str(final_schedule))
        if request is not None:
            content = content.replace(
                "<REQUESTLINK>",
                format_html(
                    "<a href='{0}'>{0}</a>".format(f"{SITE_DOMAIN}{reverse('request_view')}?id={request.id}")
                )
            )

        content = content.replace(
            "<COACH_STUDENT_LIST>",
            format_html(
                "<a href='{0}'>{0}</a>".format(f"{SITE_DOMAIN}{reverse('my_students')}"))
        )

        if user.profile.account_type == "a":
            content = content.replace("<BALANCE>", str(user.profile.studentaccount.balance))
        content = content.replace(
            "<CONFIRMLINK>",
            format_html(
                '<a href="{0}">{0}</a>'.format(
                    "{}{}?key={}".format(
                        SITE_DOMAIN, reverse("confirmation"), user.profile.secret_key
                    )
                )
            ),
        )
        content = content.replace("\n", "<br/>")
        return content

    def send(self, user: User, bcc=None, **kwargs):
        """Sends the mail to the given user with the given people in bcc

        Args:
            user (User): The user to send the mail to
            bcc ([str], optional): A list of addresses to send the mail to as bcc. Defaults to None.
        """
        formatted_content = self.formatted_content(user, **kwargs)

        html_message = render_to_string(
            "mail.html",
            {
                "title": self.clean_header,
                "content": formatted_content,
                "error_mail": "",
                "site_see_link": "{}{}".format(
                    SITE_DOMAIN, reverse("soon_view")
                ),
            },
        )

        to = [user.email]
        from_email = "CAD - Cours a domicile <{}>".format(EMAIL_HOST_USER)

        if bcc is not None:
            msg = EmailMultiAlternatives(
                self.clean_header, self.formatted_content(user), from_email, to, bcc=bcc
            )
        else:
            msg = EmailMultiAlternatives(
                self.clean_header, self.formatted_content(user), from_email, to
            )
        msg.attach_alternative(html_message, "text/html")
        if not DEBUG:
            msg.send()
        else:
            logging.warning(f"Mail {self.id} not sent because settings.DEBUG is True")

        self._sendAsNotif(
            user=user,
            title=self.clean_header,
            content=formatted_content
        )

        # Duplicates the email, setting it as "sent" email
        self.pk = None
        self.role = "i"
        self.to = user
        self.save()

    @property
    def clean_header(self) -> str:
        """Cleans the subject of the mail

        Returns:
            str: The cleaned subject
        """
        return str(self.subject).replace("\n", "")

    def __str__(self):
        return self.name


class Message(models.Model):
    """The Message model"""

    subject = models.TextField(null=False, default="No subject")
    content = models.TextField(null=False)
    contact_mail = models.CharField(max_length=250)
    seen = models.BooleanField(default=False)

    def rendered(self) -> str:
        """Renders a message as html string using the mail template

        Returns:
            str: The html content of the message as string
        """
        html_message = render_to_string(
            "mail.html",
            {
                "title": "Nouveau message d'un utilisateur de CAD",
                "content": "<h2>{}</h2><br/>{}".format(self.subject, self.content),
                "error_mail": "null",
                "site_see_link": "null",
            },
        )

        return html_message

    def send_as_mail(self):
        """Sends the message as mail to the CAD mailbox"""
        logging.debug(
            "Sending mail : {}\n{}\n\n{}".format(
                self.subject, self.content, self.contact_mail
            )
        )

        html_message = render_to_string(
            "mail.html",
            {
                "title": "Nouveau message d'un utilisateur de CAD",
                "content": "<h2>{}</h2><br/>{}".format(self.subject, self.content),
                "error_mail": "",
                "site_see_link": "{}{}?id={}".format(
                    SITE_DOMAIN, reverse("message_admin_view"), self.pk
                ),
            },
        )

        to, _ = MailingList.objects.get_or_create(id=1)
        from_email = "CAD - Cours a domicile <{}>".format(EMAIL_HOST_USER)
        to = [user.email for user in to.users.all()]
        msg = EmailMultiAlternatives(self.subject, self.content, from_email, to)
        msg.attach_alternative(html_message, "text/html")
        if not DEBUG:
            msg.send()
        else:
            logging.warning(
                f"Message {self.id} not send because settings.DEBUG is True"
            )


class MailingList(models.Model):
    """Represents a list of people that will receive a certain selection of email"""

    users = models.ManyToManyField(User, verbose_name="Utilisateurs intéréssés")
    name = models.CharField(max_length=100)
