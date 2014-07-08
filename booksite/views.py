import os
import json
from json import JSONEncoder
from json import JSONDecoder
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
from dropbox import client, rest, session
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt, csrf_protect

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
    logger.debug("hello book detail")
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

    
def dropbox_integration(request, book_id):
    APP_KEY = 'nnts9944yfscuhd'
    APP_SECRET = '79wvcdjq6m0sr9q'
    ACCESS_TYPE = 'app_folder'
        
    if request.method == 'POST':
        base_path=os.path.dirname(os.path.abspath(__file__))
        config_path=os.path.join(os.path.join(base_path, 'temp_files'), "config.txt")
        logger.debug("Base path="+base_path)
        logger.debug("Config path="+config_path)
        content=[]
        if os.path.exists(config_path):
            logger.debug("Config.txt var")
            with open(config_path) as the_file:
                content = the_file.readlines()
        else:
            logger.debug("Config.txt yok")
            with open(config_path, 'w') as the_file:
                the_file.write(APP_KEY)
                the_file.write('|')
                the_file.write(APP_SECRET)
                
        config_key=content[0].split('|')[0]
        config_secret=content[0].split('|')[1]

        callback = "http://127.0.0.1:8000/booksite/file_upload"
         
        global sess
        sess = session.DropboxSession(config_key, config_secret, ACCESS_TYPE)
        request_token = sess.obtain_request_token()
        request.session['request_token']=json.dumps(request_token.__dict__)
        logger.debug("req_ses="+request.session['request_token'])
        
        url = sess.build_authorize_url(request_token, oauth_callback=callback)
        
        request.session['book_id']=book_id
        
        return HttpResponseRedirect(url)
    return HttpResponseRedirect("http://127.0.0.1:8000/booksite/")

@csrf_protect   
def file_upload(request):
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(os.path.join(base_path, 'temp_files'), "config.txt")
    logger.debug("Base path=" + base_path)
    logger.debug("Config path=" + config_path)
    content = []
    if os.path.exists(config_path):
        with open(config_path) as the_file:
           content = the_file.readlines()
    else:
        logger.debug("Config.txt dosyasi bulunamadi.")
             
    config_key = content[0].split('|')[0]
    config_secret = content[0].split('|')[0]
         
    ACCESS_TYPE = 'app_folder'
         
    sess = session.DropboxSession(config_key, config_secret, ACCESS_TYPE)
      
    b_id = request.session['book_id']
    logger.debug("File upload fonksiyonu book id=" + str(b_id))
          
    book = get_object_or_404(Book, pk=1)  # book_id olarak 1 verdim.
    request_token = JSONDecoder(object_hook=from_json).decode(request.session['request_token'])
    logger.debug("REQUEST_TOKEN="+str(request_token))
    access_token = sess.obtain_access_token(request_token)
    #access_token="ACT3u50VHu4AAAAAAAAAMW3N2F5cPZbRkAhJAE7DM4MKc-JfeUHMFsak6n1TBJWN"
    
    logger.debug("ACCESS_TOKEN="+str(access_token))
    client1 = client.DropboxClient(sess)
    try:
        base_path1 = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_path1, "udacity.txt"), "rb") as fh:
             res = client1.put_file("udacity.txt", fh)
    except Exception, e:
        logger.debug("ERROR: " + str(e))
         
    url = "http://127.0.0.1:8000/booksite/books/12/detail/"
    return HttpResponseRedirect(url)   


def from_json(json_object):
    secret=""
    key=""
    if 'secret' in json_object:
        secret=json_object['secret']
    if 'key' in json_object:
        key=json_object['key']
    logger.debug(secret+" ---- "+key)
    return session.OAuthToken(json_object['secret'], json_object['key'])
