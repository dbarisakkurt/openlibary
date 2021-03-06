#-*- coding: utf-8 -*-

from django.db import models
from django import forms
import datetime

#version beta 0.2
#sendmail ile mail yollanabilsin
#ERROR:  HTTPSConnectionPool(host='api-content.dropbox.com', port=443): Read timed out.

#rango
#daha sonra
#TODO: django sitemap yap.
#TODO: rss okuyucusu yap.
#TODO: eklenme tarihi, alfabetik vs. gibi sıralama türleri ekle.
#TODO: son eklenen kitaplar sayfası yap.
#TODO: ana sayfada rasgele kitapları image slider olarak listele
#TODO: twitter hesabını sitenin bir yerinde listele
#TODO: admin lisans belirtilmemiş gelsin.
#TODO: admin sayfası logo değiştir.
#TODO: haber ekleme kısmının olduğu haberler kısmını koy
#TODO: en çok indirilenler sayfası yap.
#TODO: google arama entegrasyon veya kendin yap.
#TODO: x serisi bölümü yap. (dünya tarihi serisi, veri koruma serisi vs. gibi)
#TODO: fb, twitter paylaş linki ekle.
#TODO: iletişim formunu güzelleştir, bootstrap stilleri
#TODO: onedrive a yükleme desteği
#TODO: google drive a yükleme desteği



class Genre(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name
    
class License(models.Model):
    name = models.CharField(max_length=100)
    english_license = models.CharField(max_length=100)
    turkish_license = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
class Language(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
    
class Writer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    website = models.CharField(max_length=40)
    biography = models.TextField(max_length=200)
    birthdate = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.first_name+" "+self.last_name
    

class Author(Writer):
    pass

class Translator(Writer):
    pass

class Book(models.Model):

    def get_cover_name(instance, file_name):
        year=datetime.datetime.today().year
        month=datetime.datetime.today().month
        day=datetime.datetime.today().day
        hour=datetime.datetime.today().hour
        minute=datetime.datetime.today().minute
        second=datetime.datetime.today().second
        return "cover_"+unicode(str(year)+str(month)+str(day)+str(hour)+str(minute)+str(second))+file_name

    def get_book_name(instance, file_name):
        year=datetime.datetime.today().year
        month=datetime.datetime.today().month
        day=datetime.datetime.today().day
        hour=datetime.datetime.today().hour
        minute=datetime.datetime.today().minute
        second=datetime.datetime.today().second
        return "book_"+unicode(str(year)+str(month)+str(day)+str(hour)+str(minute)+str(second))+file_name

    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    translators = models.ManyToManyField(Translator, null=True, blank=True)
    page_number = models.CharField(max_length=10)
    genres = models.ManyToManyField(Genre)
    book_url = models.CharField(max_length=100)
    date_created = models.DateField(auto_now=True) 
    created_by = models.CharField(max_length=100) 
    cover_path = models.ImageField(upload_to=get_cover_name) 
    book_file = models.FileField(upload_to=get_book_name)
    short_summary = models.CharField(max_length=400)
    long_summary = models.CharField(max_length=800)
    orginal_title = models.CharField(max_length=100)
    orginal_language = models.ForeignKey(Language, related_name='olang', default=1)
    language = models.ForeignKey(Language, related_name='lang', default=1)
    license = models.ForeignKey(License)
    publish_date = models.DateField(auto_now=True)
    book_size = models.FloatField()
    additional_note = models.CharField(max_length=400)

    def __unicode__(self):
        return self.title


class ContactForm(forms.Form):
    sender = forms.EmailField(max_length=100, required=False, label="E-posta:")
    subject = forms.CharField(max_length=100, label="Konu:")
    message = forms.CharField(widget=forms.Textarea, label="İleti:")
 