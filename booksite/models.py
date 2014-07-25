#-*- coding: utf-8 -*-

from django.db import models
from django import forms
import datetime



#{% static "admin/css/base.css" %} /admini acmiyor pythonanywherede.
#resim ve kitap dosya url'leri 127.0.0.1 olarak kalmış galiba.
#change_name ve change_name2 fonksiyonları ismini değiştir.
#TODO: filter genre kitabı sağa al
#TODO: python ile kitap listesini pdf olarak dışarı aktarma. https://docs.djangoproject.com/en/dev/howto/outputting-pdf/
#SSS soruları kalınlaştır ve mail atılan adresi değiştir.




#safsata kılavuzu, emo, ozemre, istihza, http://programarcadegames.com/index.php?lang=tr

#TODO: license modeline türkçe ve ingilizce web linki ekle

#version2:
#TODO: iletişim formunu güzelleştir, bootstrap stilleri
#TODO: base template kullan.
#TODO: eklenme tarihi, alfabetik vs. gibi sıralama türleri ekle.
#TODO: admin sayfasında short, long summary text area yap.
#TODO: haber ekleme kısmının olduğu haberler kısmını koy
#TODO: pep8.py denetimi ekle
#TODO: son eklenen 5 kitabı ana sayfada listele
#TODO: twitter hesabını sitenin bir yerinde listele
#TODO: fb, twitter paylaş linki ekle.
#TODO: django sitemap yap.
#TODO: filter genreyi all book list ile beraber yap.

#daha sonra:
#TODO: kitap url'lerini düzelt, dinamik olsun.
#TODO: filter sayfasına pager ekle.
#TODO: is_new alanı ekle. is_new true ise yanına new badge'i ekle ileride.
#TODO: admin sayfasında dil default türkçe, lisans belirtilmemiş gelsin.
#TODO: google arama entegrasyon veya kendin yap.
#TODO: x serisi bölümü yap. (dünya tarihi serisi, veri koruma serisi vs. gibi)

class Genre(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name
    
class License(models.Model):
    name = models.CharField(max_length=100)
    
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
        return "cover_"+unicode(str(year)+str(month)+str(day)+str(hour)+str(minute)+str(second))+file_name

    def change_name2(instance, file_name):
        year=datetime.datetime.today().year
        month=datetime.datetime.today().month
        day=datetime.datetime.today().day
        hour=datetime.datetime.today().hour
        minute=datetime.datetime.today().minute
        second=datetime.datetime.today().second
        return "book_"+unicode(str(year)+str(month)+str(day)+str(hour)+str(minute)+str(second))+file_name

    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    page_number = models.CharField(max_length=10)
    genres = models.ManyToManyField(Genre)
    book_url = models.CharField(max_length=100)
    date_created = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=100)
    cover_path = models.ImageField(upload_to=change_name)
    book_file = models.FileField(upload_to=change_name2)
    short_summary = models.CharField(max_length=400)
    long_summary = models.CharField(max_length=800)
    orginal_title = models.CharField(max_length=100)
    orginal_language = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    license = models.ForeignKey(License)
    publish_date = models.DateField(auto_now=True)
    book_size = models.FloatField()
    additional_note = models.CharField(max_length=400)

    def __unicode__(self):
        return self.title


class ContactForm(forms.Form):
    sender = forms.EmailField(required=False, label="E-posta:")
    subject = forms.CharField(max_length=100, label="Konu:")
    message = forms.CharField(widget=forms.Textarea, label="İleti:")




