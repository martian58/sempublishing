from django.contrib import admin
from .models import Book, Author, Category, ContactMessage
# Register your models here.

from parler.admin import TranslatableAdmin

class BookAdmin(TranslatableAdmin):
    list_display = ('title', 'price')

class CategoryAdmin(TranslatableAdmin):
    list_display = ('name',)
    search_fields = ('translations__name',)

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ContactMessage)