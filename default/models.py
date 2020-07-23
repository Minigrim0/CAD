# -*- coding: utf-8 -*-

import logging

from django.core.mail import send_mail
from django.db import models

from cad.settings import EMAIL_HOST_USER


class Article(models.Model):
    name = models.CharField(
        max_length=100, default="Article",
        verbose_name="Nom de l'article")
    title = models.TextField(null=True)
    subtitle = models.TextField(null=True)
    content = models.TextField(null=True)
    date = models.DateTimeField(
        auto_now_add=True, auto_now=False,
        verbose_name="Date de modification")

    def __str__(self):
        return self.name


class Mail(models.Model):
    name = models.CharField(
        max_length=150, default="Mail template",
        verbose_name="Nom du template")
    subject = models.CharField(
        max_length=150, default="CAD - Cours à domicile", verbose_name="Sujet")
    content = models.TextField(default="None", verbose_name="Contenu")

    choices = (
        ('a', 'verification de l\'adresse mail'),
        ('b', 'mail de bienvenue'),
        ('c', 'proposition desinscription'),
        ('d', 'solde dangereux'),
        ('e', 'proposition de mission'),
        ('f', 'attribution de mission'),
        ('g', 'mission attribuée à un autre coach'),
        ('h', 'Template non automatique'),
    )

    role = models.CharField(
        max_length=1, choices=choices, verbose_name="Role du mail")

    def formatted_content(self, user):
        content = str(self.content)
        content = content.replace("<LASTNAME>", str(user.last_name))
        content = content.replace("<FIRSTNAME>", str(user.first_name))
        content = content.replace("<BIRTHDATE>", str(user.profile.birthDate))
        content = content.replace("<COURSES>", str(user.profile.courses))
        content = content.replace("<SCHOOLLEVEL>", str(user.profile.birthDate))
        content = content.replace("<SECRETKEY>", str(user.profile.secret_key))
        content = content.replace(
            "<CONFIRMLINK>",
            "127.0.0.1:8000/inscription/confirm/" + user.profile.secret_key)
        return content

    @property
    def clean_header(self):
        return str(self.subject).replace("\n", "")

    def __str__(self):
        return self.name


class Message(models.Model):
    subject = models.TextField(null=False, default="No subject")
    content = models.TextField(null=False)
    contact_mail = models.CharField(max_length=250)

    def send_as_mail(self):
        logging.debug("Sending mail : {}\n{}\n\n{}".format(self.subject, self.content, self.contact_mail))
        send_mail(
            self.subject, "{}\n\n{}".format(self.content, self.contact_mail),
            EMAIL_HOST_USER, ['cadcoursadomicile@gmail.com'])
