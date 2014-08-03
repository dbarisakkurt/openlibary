# -*- coding: utf-8 -*-

import os
import json
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  
from booksite.models import Book, Genre, Author
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from models import ContactForm
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from dropbox import client, rest, session
import requests
import oauth2 as oauth
import cgi
from common.utility import utility

logger = logging.getLogger(__name__)
 
def all_books(request):
    all_books_list = Book.objects.all().order_by('title')[:]
    paginator = Paginator(all_books_list, 10)  # Show 10 books per page
    all_books = getBookNumber()
    
    all_genres_list = Genre.objects.all().order_by('name')[:]
    
    page = request.GET.get('page')
    try:
        all_books_list = paginator.page(page)
    except PageNotAnInteger:
        all_books_list = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_books_list = paginator.page(paginator.num_pages)
        
    context = {'all_books_list': all_books_list, 'all_genres_list': all_genres_list, 'book_number': all_books}
    return render(request, 'booksite/all_books.html', context)
    
def book_detail(request, book_id):
    if not request.session.has_key('dropbox_load1'):
        sonuc = False
    else:
        sonuc = request.session['dropbox_load1']
    book = get_object_or_404(Book, pk=book_id)
    if sonuc == True:
        request.session.pop("dropbox_load1", None)
        return render(request, 'booksite/book_detail.html', {'book': book, 'dropbox_load': True })
    else:
        return render(request, 'booksite/book_detail.html', {'book': book, 'dropbox_load': False })

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'booksite/author_detail.html', {'author': author})


def filter_genre(request):
    if request.method == 'GET':
        genre_number = request.GET['genre']
        books_in_genre = Book.objects.filter(genres__id=genre_number)
        genre_url = '/booksite/filter_genre/' + genre_number + '/'
        # return HttpResponseRedirect(genre_url)
        return render(request, 'booksite/filter_genre.html', {'books_in_genre': books_in_genre})
   
def send_message(request):
    context = RequestContext(request)          

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            
            send_mail(subject, message + " Gonderen: " + sender, sender, ['acikkiletisim@gmail.com'])
            return render_to_response('booksite/index.html', {}, context)
        else:
            print form.errors
    else:
        form = ContactForm()

    return render_to_response('booksite/send_message.html', {'form': form}, context)

DROPBOX_ACCESS_TYPE = 'app_folder'
    
def dropbox_login(request, book_id):
    #callback_url = 'http://www.acikkutuphane.org/dropbox_authenticate'
    callback_url='http://127.0.0.1:8000/dropbox_authenticate'
    tokens = utility.getDropboxAppKeyAndSecret()
    
    print tokens[0]
    print tokens[1]
    # Step 1. Get a request token from Dropbox.
    sess = session.DropboxSession(tokens[0], tokens[1], DROPBOX_ACCESS_TYPE)
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token, oauth_callback=callback_url)

    request.session['request_token'] = request_token
    request.session['session'] = sess
    request.session['book_id'] = book_id
    request.session['callback_url'] = request.get_full_path()
    return HttpResponseRedirect(url)


def dropbox_authenticate(request):
    print "auth fonk."
    request_token = request.session['request_token']
    sess = request.session['session']
     
    access_token = sess.obtain_access_token(request_token)
    client1 = client.DropboxClient(sess)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    # dosya yukle
    b_id = request.session['book_id']
    book1 = get_object_or_404(Book, pk=b_id)
    temp_file_path = os.path.join(base_path, 'documents')
    
    print "Kitap yol:" + str(book1.book_file)
    
    book_path = os.path.join(temp_file_path, str(book1.book_file))
    print "Book path=" + str(book_path)
    
    try:
        with open(book_path, "rb") as fh:
            print "Dosya acildi"
            print "basename=" + str(os.path.basename(book_path))
            res = client1.put_file(os.path.basename(book_path), fh)
            print "Dosya yuklendi: ", res
    except Exception, e:
            print "ERROR: ", e
            
    book = get_object_or_404(Book, pk=b_id)
    #callback_url = "http://www.acikkutuphane.org/books/" + str(b_id) + "/detail/"
    callback_url="http://127.0.0.1:8000/books/"+str(b_id)+"/detail/"
    dResult = True
    request.session['dropbox_load1'] = dResult
    return redirect(callback_url)


def getBookNumber(category='all'):
    if category == 'all':
        all_books_list = Book.objects.all()[:]
        return len(all_books_list)
    else:
        my_genre = Genre.objects.get(name=category)
        print my_genre.id
        all_books_by_genre = Book.objects.filter(genres=my_genre.id)
        return len(all_books_by_genre)
    
def output_pdf_list(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="acikkutuphane.pdf"'

    p = canvas.Canvas(response)

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    p.setFont('Vera', 16)
    all_books_list = Book.objects.all()[:]
    coordx, coordy = 100, 760
    
    p.drawString(200, 800, "Açık Kütüphane Kitap Listesi")
    p.setFont('Vera', 11)
    
    counter = 1
    for book in all_books_list:
        p.drawString(coordx, coordy, str(counter) + "- " + book.title)
        coordy -= 20
        counter += 1
        if coordy == 100:
            p.showPage()
            p.setFont('Vera', 11)
            coordy = 800
    
    p.save()
    return response
