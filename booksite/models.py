#-*- coding: utf-8 -*-

from django.db import models
from django import forms
import datetime


class Genre(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

    def __unicode__(self):
        return self.first_name+" "+self.last_name


class Book(models.Model):

    def change_name(instance, file_name):
        return "documents/covers/"+unicode(datetime.datetime.now())+file_name

    def change_name2(instance, file_name):
        return "documents/docs/"+unicode(datetime.datetime.now())+file_name

    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    page_number = models.CharField(max_length=10)
    genres = models.ManyToManyField(Genre)
    book_url = models.CharField(max_length=100)
    date_created = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100)
    cover_path = models.ImageField(upload_to=change_name)
    book_file = models.FileField(upload_to=change_name2)

    def __unicode__(self):
        return self.title





class ContactForm(forms.Form):
    sender = forms.EmailField(required=False, label="E-posta:")
    subject = forms.CharField(max_length=100, label="Konu:")
    message = forms.CharField(widget=forms.Textarea, label="İleti:")



