# urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('add-word/', views.add_word_htmx, name='add_word_htmx'),
]
