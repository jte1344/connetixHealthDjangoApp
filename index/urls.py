from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('interactions/', views.interactions, name='interactions'),
    path('interactions/<str:medication>', views.interactionsParam, name='interactionsParam'),
    path('local/<str:medication>', views.local, name='local'),
    path('mapsAPI/<str:location>', views.mapsAPI, name='mapsAPI'),
    path('interactionsAPI/<str:medication>', views.interactionsAPI, name='interactionsAPI'),
]
