from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pubmed_journal/<str:journal_title>/', views.pubmed_journal, name='pubmed_journal'),
    path('author/<str:author_name>/', views.author, name='author'),
]