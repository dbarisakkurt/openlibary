from django.contrib import admin
from django import forms
from booksite.models import Book, Genre, Author, License, Language, Translator

class BookForm( forms.ModelForm ):
    short_summary = forms.CharField( widget=forms.Textarea )
    long_summary = forms.CharField( widget=forms.Textarea )
    additional_note = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = Book

class BookAdmin(admin.ModelAdmin):
    form=BookForm
    filter_horizontal = ('authors', 'translators', 'genres')
    list_display = ('title', 'page_number', 'book_url', 'book_size')
    ordering = ('title',)

admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(License)
admin.site.register(Language)
admin.site.register(Translator)



