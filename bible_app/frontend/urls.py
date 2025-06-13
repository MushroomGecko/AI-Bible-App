from django.urls import path
from . import views

app_name = 'frontend'  # Namespacing the URLs

urlpatterns = [
    path('<str:book>-<str:chapter>-<str:version>/', views.bible_book_view, name='bible_book_view'),
    path('<str:book>-<str:chapter>/', views.bible_book_fix_view, name='bible_book_fix'),
    path('', views.home_view, name='home_page'),

] 