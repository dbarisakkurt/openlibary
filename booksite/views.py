from django.http import HttpResponse
from booksite.models import Book, Genre
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from models import ContactForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger(__name__)

#def index(request):
#    return HttpResponse("Hello, world. You're at the poll index.")

#def about(request):
#    return HttpResponse("This is about page.")

def all_books(request):
    all_books_list = Book.objects.all().order_by('-title')[:]
    all_genres_list = Genre.objects.all().order_by('-name')[:]
    
    context = {'all_books_list': all_books_list, 'all_genres_list': all_genres_list}
    return render(request, 'booksite/all_books.html', context)
    
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'booksite/book_detail.html', {'book': book})



def filter_genre(request):
    if request.method == 'GET':
        genre_number=request.GET['genre']
        books_in_genre=Book.objects.filter(genres__id=genre_number)
        genre_url='/booksite/filter_genre/'+genre_number+'/'
        #return HttpResponseRedirect(genre_url)
        return render(request, 'booksite/filter_genre.html', {'books_in_genre': books_in_genre})
   
    #if request.method == 'POST':
    #selected_item = get_object_or_404(Genre, pk=genre_id)
        #return render_to_response('booksite/all_books.html', {'books_in_genre':books_in_genre}, context_instance =  RequestContext(request),)
    #return render(request, 'booksite/filter_genre.html', {'books_in_genre': books_in_genre})

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
