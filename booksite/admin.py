from django.contrib import admin
from booksite.models import Book
from booksite.models import Genre
from booksite.models import Author
from booksite.models import License
from booksite.models import Language


admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(License)
admin.site.register(Language)



