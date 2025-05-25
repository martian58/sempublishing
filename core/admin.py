from django.contrib import admin
from .models import Book, Author, Category, ContactMessage
# Register your models here.

from parler.admin import TranslatableAdmin

class BookAdmin(TranslatableAdmin):
    search_fields = ('translations__title', 'translations__description', 'isbn_number')
    list_display = ('title','isbn_number','price')

class CategoryAdmin(TranslatableAdmin):
    list_display = ('name',)
    search_fields = ('translations__name',)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')   # columns in the admin list view
    search_fields = ('name', 'email', 'message')     # search bar for these fields
    list_filter = ('created_at',)                                # filter by date
    ordering = ('-created_at',)                                  # default ordering


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')                     # columns in the admin list view
    search_fields = ('name', 'surname')                    # searchable fields
    ordering = ('name', 'surname')                         # default ordering (alphabetical)



admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Author, AuthorAdmin)
