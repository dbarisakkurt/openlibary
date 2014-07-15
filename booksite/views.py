import os
import json
from json import JSONEncoder
from json import JSONDecoder
import oauth2 as oauth
import cgi
import requests
from django.http import HttpResponse
from booksite.models import Book, Genre, Author
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from models import ContactForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from dropbox import client, rest, session
from ctypes.test.test_random_things import callback_func


logger = logging.getLogger(__name__)


 
def all_books(request):
    all_books_list = Book.objects.all().order_by('-title')[:]
    paginator = Paginator(all_books_list, 10) # Show 10 books per page
    
    all_genres_list = Genre.objects.all().order_by('-name')[:]
    
    page = request.GET.get('page')
    try:
        all_books_list = paginator.page(page)
    except PageNotAnInteger:
        all_books_list = paginator.page(1)        # If page is not an integer, deliver first page.
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_books_list = paginator.page(paginator.num_pages)
        
    context = {'all_books_list': all_books_list, 'all_genres_list': all_genres_list}
    return render(request, 'booksite/all_books.html', context)
    
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'booksite/book_detail.html', {'book': book})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'booksite/author_detail.html', {'author': author})


def filter_genre(request):
    if request.method == 'GET':
        genre_number=request.GET['genre']
        books_in_genre=Book.objects.filter(genres__id=genre_number)
        genre_url='/booksite/filter_genre/'+genre_number+'/'
        #return HttpResponseRedirect(genre_url)
        return render(request, 'booksite/filter_genre.html', {'books_in_genre': books_in_genre})
   
def send_message(request):
    context = RequestContext(request)          

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail('test email', 'hello world', 'dbarisakkurt@gmail.com', ['dbarisakkurt@gmail.com'])
            return render_to_response('booksite/index.html', {}, context)
        else:
            print form.errors
    else:
        form = ContactForm()

    return render_to_response('booksite/send_message.html', {'form': form}, context)

request_token_url = 'https://api.dropbox.com/1/oauth/request_token'
access_token_url = 'https://www.dropbox.com/1/oauth/authorize'

DROPBOX_APP_KEY='nnts9944yfscuhd'
DROPBOX_APP_SECRET='79wvcdjq6m0sr9q'
DROPBOX_ACCESS_TYPE = 'app_folder'

req_t=None
sess1=None
    
def dropbox_login(request):
    callback_url='http://127.0.0.1:8000/booksite/dropbox_authenticate'
    # Step 1. Get a request token from Dropbox.
    sess = session.DropboxSession(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_ACCESS_TYPE)
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token, oauth_callback=callback_url)
    
    
    print "URL="+url
    request.session['request_token']=request_token
    request.session['session']=sess
    print "session="+str(sess)

    return HttpResponseRedirect(url)



def dropbox_authenticate(request):
    print "dropbox_authenticate fonksiyonu"
    request_token=request.session['request_token']
    sess=request.session['session']
    print "session="+str(sess)
    
    print "dropbox_authenticate fonksiyonu2" 
    access_token = sess.obtain_access_token(request_token)
    print "dropbox_authenticate fonksiyonu"
    print access_token
    client1 = client.DropboxClient(sess)
    print "HESAP="+str(client1.account_info())
    
    base_path=os.path.dirname(os.path.abspath(__file__))
    #dosya yukle
    try:
        with open(os.path.join(base_path, "udacity.txt"), "rb") as fh: #os.path.join(self.path, self.filename)
            print "Dosya acildi"
            path = os.path.join(base_path, "udacity.txt")
            res = client1.put_file("udacity.txt", fh)
            print "Dosya yuklendi: ", res
    except Exception, e:
            print "ERROR: ", e
    return HttpResponseRedirect('http://127.0.0.1:8000/booksite/')



def getSize(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size


