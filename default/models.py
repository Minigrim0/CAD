#-*- coding: utf-8 -*-

from django.db import models

class Article(models.Model):
    name = models.TextField(null=False, default="Article", verbose_name="nom")
    title = models.TextField(null=True)
    subTitle = models.TextField(null=True)
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de modification")

    def __str__(self):
        return self.name
