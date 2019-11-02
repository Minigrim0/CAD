# -*- coding: utf-8 -*-

from django.db import models


class Article(models.Model):
    name = models.TextField(null=False, default="Article", verbose_name="nom")
    title = models.TextField(null=True)
    subTitle = models.TextField(null=True)
    content = models.TextField(null=True)
    date = models.DateTimeField(
        auto_now_add=True, auto_now=False, verbose_name="Date de modification")

    def __str__(self):
        return self.name


class Mail(models.Model):
    name = models.CharField(max_length=150, default="Mail template")
    subject = models.CharField(max_length=150, default="CAD - Cours à domicile")
    content = models.TextField(default="None")

    def formatted_content(self, user):
        content = self.content
        content = content.replace("<LASTNAME>", str(user.last_name))
        content = content.replace("<FIRSTNAME>", str(user.first_name))
        content = content.replace("<BIRTHDATE>", str(user.profile.birthDate))
        content = content.replace("<COURSES>", str(user.profile.courses))
        content = content.replace("<SCHOOLLEVEL>", str(user.profile.birthDate))
        content = content.replace("<SECRETKEY>", str(user.profile.secret_key))
        return content

    @property
    def clean_header(self):
        return self.subject.replace("\n", "")

    def __str__(self):
        return self.name
