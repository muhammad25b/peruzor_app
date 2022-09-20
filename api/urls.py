from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from django.contrib import admin
from . import views


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/jwt/create/', include('djoser.urls.jwt')),
    path('auth/jwt/create/', include('djoser.urls.jwt')),
    path('intro-validation/<int:user_id>/',views.intro_validator, name = 'intro_validator' ),
    path('staff-validation/<int:user_id>/',views.staff_validator, name = 'staff_validator' ),
    path('intro-test-completed/',views.intro_completed, name = 'intro_completed'),
    path('getletters/',views.get_letters, name = 'get_letters' ),
    path('letters/score/',views.letters_score, name = 'letters_score' ),
    path('getsentences/',views.get_sentences, name = 'get_sentences' ),
    path('sentences/results/',views.sentences_results, name = 'sentences_results' ),
    path('getwords/<int:level>/',views.get_words, name = 'get_words' ),
    path('words/results/',views.words_results, name = 'words_results' ),
    path('getstory/<int:test_type>/<int:level>/',views.get_story, name = 'get_story' ),
    path('story/results/',views.story_results, name = 'story_results' ),
    path('getmultipleinventory/',views.get_multiple_inventory, name = 'get_multiple_inventory'),
    path('multipleinventory/results/',views.multiple_inventory_results, name = 'multiple_inventory_results'),
    path('interestinventory/results/',views.interest_inventory_results, name = 'interest_inventory_results'),
    path('getintelliginventory/',views.get_interest_inventory, name = 'get_interest_inventory'),
    path('getuserslist/',views.get_users_list, name = 'get_users_list'),
    path('gettestsresults/<int:user_id>/',views.get_tests_list, name = 'get_tests_list'),
    path('get_sentence_results/<int:user_id>/<int:id>/',views.get_sentence_results, name = 'get_sentence_results'),
    path('get_letter_results/<int:user_id>/<int:id>/',views.get_letter_results, name = 'get_letter_results'),
    path('get_words_results/<int:user_id>/<int:id>/',views.get_words_results, name = 'get_words_results'),
    path('get_story_results/<int:user_id>/<int:id>/',views.get_story_results, name = 'get_story_results'),
    path('get_mi_results/<int:user_id>/<int:id>/',views.get_mi_results, name = 'get_mi_results'),
    path('get_ii_results/<int:user_id>/<int:id>/',views.get_ii_results, name = 'get_ii_results'),
    ]