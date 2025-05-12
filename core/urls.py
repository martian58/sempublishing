from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('books/', views.book_list, name='book_list'),
    path('category_books/<slug:slug>/', views.category_books, name='category_books'),
    path('authors/', views.author_list, name='authors'),
    path('author_detail/<int:author_id>/', views.author_detail, name='author_detail'),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('contact/', views.contact, name='contact'),
    path('publishing-policy/', views.publishing_policy, name='publishing_policy'),
    path('academic-literature/', views.academic_literature, name='academic_literature'),
    path('publish-request/', views.publish_request, name='publish_request'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove_one/<int:book_id>/', views.remove_one_from_cart, name='remove_one_from_cart'),
    path('cart/add_one/<int:book_id>/', views.add_one_to_cart, name='add_one_to_cart'),
    path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart_item_count/', views.cart_item_count, name='cart_item_count'),
    path('checkout/', views.checkout, name='checkout'),
]
