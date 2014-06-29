from django.conf.urls import patterns, url
from booksite import views
from django.conf.urls import patterns
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="booksite/index.html")),
    url(r'^about/$', TemplateView.as_view(template_name="booksite/about.html")),
    url(r'^all_books/$', views.all_books, name='all_books'),
    url(r'^books/(?P<book_id>\d+)/detail/$', views.book_detail, name='book_detail'),
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^filter_genre/$', views.filter_genre, name='filter_genre'),
    url(r'^authors/(?P<author_id>\d+)/detail/$', views.author_detail, name='author_detail')
)
