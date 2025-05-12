from django.db import models
from django.utils.text import slugify
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField('Author')
    category = models.ManyToManyField('Category')
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    published_date = models.DateField(auto_now_add=True)
    cover = models.ImageField(upload_to='covers/', blank=True)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True)
    # isbn_number = models.CharField(max_length=13)
    # is_book_open = models.BooleanField(default=False)

    def __str__(self):
        authors = self.author.all()
        authors_str = ""
        for author in authors:
            authors_str += author.name + " " + author.surname + ", "
        return self.title + " by " + authors_str[:-2]
    
    def author_names(self):
        authors = self.author.all()
        authors_str = ""
        for author in authors:
            authors_str += author.name + " " + author.surname + ", "
        return authors_str[:-2]
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    

class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    biography = models.TextField()
    photo = models.ImageField(upload_to='authors/', blank=True)

    def __str__(self):
        return self.name + " " + self.surname
    


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.quantity} of {self.book.title}"
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

        

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
