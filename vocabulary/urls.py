from django.urls import path
from . import views

app_name = 'vocabulary'

urlpatterns = [
    path('', views.vocabulary_hub, name='hub'),
    path('api/random-words/', views.api_random_words, name='api_random_words'),
    path('api/words/<int:word_id>/status/', views.api_update_word_status, name='api_update_word_status'),
    path('api/exam/start/', views.api_take_exam, name='api_take_exam'),
    path('api/exam/submit/', views.api_submit_exam, name='api_submit_exam'),
    path('add-word/', views.add_word_htmx, name='add_word_htmx'),
]
