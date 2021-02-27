from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('buttons/', views.buttons, name = 'buttons'),
    path('callserv/', views.callserv, name = 'callserv'),
    path('tests/', views.tests, name = 'tests'),
    path('articles/', views.articles, name = 'articles')
]