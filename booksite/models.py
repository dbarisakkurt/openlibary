#-*- coding: utf-8 -*-

from django.db import models
from django import forms
import datetime


#zorunlu:
#TODO: dropbox integration
#TODO: kitap listeleme sayfalarını güzelleştir: kitabın resmini sağa yasla
#TODO: kitap ayrıntısı sayfası: kitabın resmini sağa yasla, dropbox butonunu güzelleştir


#seçimli:
#TODO: iletişim formunu güzelleştir, bootstrap stilleri
#TODO: python ile kitap listesini pdf olarak dışarı aktarma.
#TODO: base template kullan.
#TODO: django sitemap yap.
#TODO: short story ve long story alanlarını genişlet admin sayfasında ve bu kısma daha çok veri girilebilsin veritabanı.
#TODO: kitapları alfabetik olarak sırala tüm kitaplar sayfasında
#TODO: eklenme tarihi, alfabetik vs. gibi sıralama türleri ekle.
#TODO: toplam kitap sayısını tüm kitaplar sayfasına ekle.
#TODO: filter sayfasına pager ekle.
#TODO: is_new alanı ekle. is_new true ise yanına new badge'i ekle ileride.

#kod refaktor:
#dizin isimleri dinamik olacak, şu an hardcode
#pep8.py denetimi ekle
#bazı dosyalar .gitignore dosyasına eklenecek



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




