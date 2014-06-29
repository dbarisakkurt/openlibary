#-*- coding: utf-8 -*-

from django.db import models
from django import forms
import datetime


#TODO: yazar için özgeçmiş, web sitesi, doğum tariyi alanı ekle.
#TODO: kitap için kısa özet, uzun özet, orjinal dil, orjinal adı, yayın tarihi, lisansı alanı ekle 
#TODO: dropbox integration



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
        year=datetime.datetime.today().year
        month=datetime.datetime.today().month
        day=datetime.datetime.today().day
        hour=datetime.datetime.today().hour
        minute=datetime.datetime.today().minute
        second=datetime.datetime.today().second
        return "documents/covers/"+unicode(str(year)+str(month)+str(day)+str(hour)+str(minute)+str(second))+file_name

    def change_name2(instance, file_name):
        year=datetime.datetime.today().year
        month=datetime.datetime.today().month
        day=datetime.datetime.today().day
        hour=datetime.datetime.today().hour
        minute=datetime.datetime.today().minute
        second=datetime.datetime.today().second
        return "documents/docs/"+unicode(str(year)+str(month)+str(day)+str(hour)+str(minute)+str(second))+file_name

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



