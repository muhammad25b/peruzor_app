from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Letters, IntroTest, UserAccounts, WordsTest, Words, LettersTest, Sentences,  Comprehensions, Comprehensions, InterestInventoryTest, InterestInventoryTestScore, MultipleIntelligenceTest, MultipleIntelligenceTestScore, SentencesTest,ComprehensionsTest,InterestInventoryTestScore

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'f_name', 'l_name', 'is_staff')


class IntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntroTest
        fields = ['user','done']

class LettersSerializer(serializers.ModelSerializer):
    class Meta():
        model  = Letters
        fields = ["letter"]

class LetterScoreSerializer(serializers.ModelSerializer):
    class Meta():
        model = LettersTest
        fields = ['score','user','test_type','test_letters','answer_letters']


class SentencesSerializer(serializers.ModelSerializer):
    class Meta():
        model = Sentences
        fields = ['sentence']

class WordsSerializer(serializers.ModelSerializer):
    class Meta():
        model = Words
        fields = ['words']


class SentencesTestSerializer(serializers.ModelSerializer):
    class Meta():
        model = SentencesTest
        fields = ['user','sentence1','sentence2','sentence3','sentence4','sentence5']


class WordsSerializer(serializers.ModelSerializer):
    class Meta():
        model = Words
        fields = ['word']

class WordsTestSerializer(serializers.ModelSerializer):
    class Meta():
        model = WordsTest
        fields = ['user','words','spoken_words','level','test_type','time']


class ComprehensionsSerializer(serializers.ModelSerializer):
    class Meta():
        model = Comprehensions
        fields = ['id','title','story','html_story']


class ComprehensionsTestSerializer(serializers.ModelSerializer):
    class Meta():
        model = ComprehensionsTest
        fields = ['user','level','test_type','story','spoken_story','time','questions_list','answers_list']



class MultipleIntelligenceTestScoreSerializer(serializers.ModelSerializer):
    class Meta():
        model = MultipleIntelligenceTestScore
        fields = ['linguistic', 'logical_mathematical', 'musical', 'spatial','bodily', 'intra_personal', 'inter_personal','user']


class InterestInventoryTestScoreSerializer(serializers.ModelSerializer):
    class Meta():
        model = InterestInventoryTestScore
        fields = ['user','score']