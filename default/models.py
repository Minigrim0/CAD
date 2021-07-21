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
        ("a", "verification de l'adresse mail"),
        ("b", "mail de bienvenue"),
        ("c", "proposition desinscription"),
        ("d", "solde dangereux"),
        ("e", "proposition de mission"),
        ("f", "attribution de mission"),
        ("g", "mission attribuée à un autre coach"),
        ("h", "Template non automatique"),
        ("i", "Message envoyé"),
    )

    role = models.CharField(max_length=1, choices=choices, verbose_name="Role du mail")
    to = models.ForeignKey(User, null=True, verbose_name="Envoyé à", on_delete=models.CASCADE)

    def formatted_content(self, user: User) -> str:
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

    def send(self, user: User, bcc=None):
        """Sends the mail to the given user with the given people in bcc

        Args:
            user (User): The user to send the mail to
            bcc ([type], optional): A list of addresses to send the mail to as bcc. Defaults to None.
        """
        html_message = render_to_string(
            "mail.html",
            {
                "title": self.clean_header,
                "content": self.formatted_content(user),
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
            logging.warning(f"Mail {self.id} not send because settings.DEBUG is True")

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
