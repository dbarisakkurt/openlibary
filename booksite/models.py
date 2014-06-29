#-*- coding: utf-8 -*-

from django.db import models
from django import forms
import datetime


#zorunlu:
#TODO: dropbox integration
#TODO: kitap listeleme sayfasını güzelleştir.
#TODO: kitap ayrıntısı sayfasını güzelleştir.
#TODO: yazar ayrıntısı sayfasını güzelleştir.
#TODO: pagination türkçe yap.
#TODO: hakkında sayfasını güzelleştir; sekme vs. olabilir.
#TODO: kullanım koşulları: project gutenberg terms of use benzeri
#TODO: django sitemap yap.

#seçimli:
#TODO: iletişim formunu güzelleştir, bootstrap stilleri
#TODO: python ile kitapları pdf olarak dışarı aktarma.


#kod refaktor:
#dizin isimleri dinamik olacak, şu an hardcode
#pep8.py denetimi ekle



class Genre(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    website = models.CharField(max_length=40)
    biography = models.TextField(max_length=200)
    birthdate = models.DateField(auto_now=True)
    

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
    short_summary = models.CharField(max_length=100)
    long_summary = models.CharField(max_length=300)
    orginal_title = models.CharField(max_length=100)
    orginal_language = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    license = models.CharField(max_length=100)
    publish_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.title





class ContactForm(forms.Form):
    sender = forms.EmailField(required=False, label="E-posta:")
    subject = forms.CharField(max_length=100, label="Konu:")
    message = forms.CharField(widget=forms.Textarea, label="İleti:")




