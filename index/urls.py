from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('interactions/', views.interactions, name='interactions'),
    path('local/<str:medication>', views.local, name='local'),
    path('interactionsAPI/<str:medication>', views.interactionsAPI, name='interactionsAPI'),
]
