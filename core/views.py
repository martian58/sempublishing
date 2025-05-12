from django.shortcuts import render
from .models import Book, Author, Category
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, OrderItem
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ContactMessage
from .forms import ContactMessageForm
# Create your views here.

def home(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(books, 12)  # Show 12 books per page
    page_number = request.GET.get('page')
    page_books = paginator.get_page(page_number)

    home_data = {
        'books': page_books,
        'categories': categories,
        'query': query,
    }

    return render(request, 'core/home.html', {'home_data': home_data})

def about(request):
    return render(request, 'core/about.html')

def cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    cart_items = OrderItem.objects.filter(session_key=session_key)
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, 'core/cart.html', {'cart_items': cart_items, 'total_price': total_price})



def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    order_item, created = OrderItem.objects.get_or_create(book=book, session_key=session_key)
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('home')

def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    session_key = request.session.session_key
    if session_key:
        order_item = get_object_or_404(OrderItem, book=book, session_key=session_key)
        order_item.delete()
    return redirect('cart')

def remove_one_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    session_key = request.session.session_key
    if session_key:
        order_item = get_object_or_404(OrderItem, book=book, session_key=session_key)
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()
    return redirect('cart')

def add_one_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    order_item, created = OrderItem.objects.get_or_create(book=book, session_key=session_key)
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('cart')

def cart_item_count(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    count = OrderItem.objects.filter(session_key=session_key).count()
    return JsonResponse({'count': count})


def checkout(request):
    session_key = request.session.session_key
    cart_items = OrderItem.objects.filter(session_key=session_key)
    if request.method == 'POST':
        # Process payment here (integration with a payment gateway would go here)
        cart_items.delete()  # Clear the cart after successful payment
        return redirect('home')
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, 'core/checkout.html', {'cart_items': cart_items, 'total_price': total_price})



# Auth

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered')
            else:
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'core/register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'core/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')


# Book and Author

def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(books, 12)  # Show 12 books per page
    page_number = request.GET.get('page')
    page_books = paginator.get_page(page_number)
    books_data = {
        'books': page_books,
        'categories': categories,
        'query': query,
    }
    return render(request, 'core/book_list.html', {'books_data': books_data})


def category_books(request, slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category)
    paginator = Paginator(books, 12)  # Show 12 books per page
    page_number = request.GET.get('page')
    page_books = paginator.get_page(page_number)
    books_data = {
        'books': page_books,
        'categories': categories
    }
    return render(request, 'core/book_list.html', {'books_data': books_data})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    related_books = Book.objects.filter(category__in=book.category.all()).exclude(id=book_id).distinct()
    paginator = Paginator(related_books, 4)  # Show 4 related books per page
    page_number = request.GET.get('page')
    page_related_books = paginator.get_page(page_number)

    return render(request, 'core/book_detail.html', {
        'book': book,
        'related_books': page_related_books
    })

def author_list(request):
    query = request.GET.get('q')
    if query:
        authors = Author.objects.filter(name__icontains=query) | Author.objects.filter(surname__icontains=query)
    else:
        authors = Author.objects.all()
    
    paginator = Paginator(authors, 12)  # Show 12 authors per page
    page_number = request.GET.get('page')
    page_authors = paginator.get_page(page_number)

    return render(request, 'core/author_list.html', {'page_authors': page_authors, 'query': query})

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = Book.objects.filter(author=author)
    return render(request, 'core/author_detail.html', {'author': author, 'books': books})

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = ContactMessageForm()
    return render(request, 'core/contact.html', {'form': form})


# Extra

def publishing_policy(request):
    return render(request, 'core/publishing_policy.html')

def academic_literature(request):
    return render(request, 'core/academic_literature.html')

def publish_request(request):
    return render(request, 'core/publish_request.html')