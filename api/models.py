from django.contrib.auth import get_user_model
from django.utils import timezone
import django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from tinymce import models as tinymce_models


class UserAccountManager(BaseUserManager):
    def create_superuser(self, email, username, f_name,l_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, f_name, l_name, password, **other_fields)

    def create_user(self, email, username, f_name, l_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
        if not username:
            raise ValueError(_('You must provide a Username'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          f_name=f_name, l_name = l_name,**other_fields)
        user.set_password(password)
        user.save()
        return user



class UserAccounts(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    f_name = models.CharField(max_length=255, default= None)
    l_name = models.CharField(max_length = 255, default= None)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='date joined')
    last_login = models.DateTimeField(default=timezone.now, verbose_name='last login')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','f_name','l_name']

    def __get_full_name(self):
        return self.f_name + "  " + self.l_name

    def __get_short_name(self):
        return self.f_name

    def __str__(self):
        return self.username

User = get_user_model()


class IntroTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)


class Letters(models.Model):
    letter = models.CharField(max_length=1)




class Words(models.Model):
    levels = [("Pre Primer", "Pre Primer"),
              ("Primer", "Primer"),
              ("Level 1", "Level 1"),
              ("Level 2", "Level 2"),
              ("Level 3", "Level 3"),
              ("Level 4", "Level 4"),
              ("Level 5", "Level 5"),
              ("Level 6", "Level 6")]
    word = models.CharField(max_length=50)
    level  = models.CharField(max_length=255,choices = levels,default=None)



class Sentences(models.Model):
    sentence = models.CharField(max_length=500)



class Comprehensions(models.Model):
    levels = [("Pre Primer", "Pre Primer"),
              ("Primer", "Primer"),
              ("Level 1", "Level 1"),
              ("Level 2", "Level 2"),
              ("Level 3", "Level 3"),
              ("Level 4", "Level 4"),
              ("Level 5", "Level 5"),
              ("Level 6", "Level 6")]
    title = models.CharField(max_length=255,blank=True)
    story = models.TextField()
    html_story = tinymce_models.HTMLField(default = None)
    level = models.CharField(max_length=255, choices=levels,default=None)
    test_type = models.CharField(max_length=255, choices=[("Pre Test", "Pre Test"), ("Post Test", "Post Test")])



class Questions(models.Model):
    questions = models.CharField(max_length=500)
    answer = models.CharField(max_length=200)
    answer2 = models.CharField(max_length=200, default="N/A")
    answer3 = models.CharField(max_length=200, default="N/A")
    answer4 = models.CharField(max_length=200, default="N/A")
    comprehension = models.ForeignKey('Comprehensions', on_delete=models.CASCADE)



class MultipleIntelligenceTest(models.Model):
    intelligence_type = [
        ("A", "Linguistic"),
        ("B", "Logical- Mathematical"),
        ("C", "Musical"),
        ("D", "Spatial"),
        ("E", "Bodily Kinesthetic"),
        ("F", "Intra Personal"),
        ("G", "Inter Personal"),
    ]
    question = models.CharField(max_length=500)
    type = models.CharField(max_length=20, choices=intelligence_type)



class MultipleIntelligenceTestScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    linguistic = models.CharField(max_length=100)
    logical_mathematical = models.CharField(max_length=100)
    musical = models.CharField(max_length=100)
    spatial = models.CharField(max_length=100)
    bodily = models.CharField(max_length=100)
    intra_personal = models.CharField(max_length=100)
    inter_personal = models.CharField(max_length=100)
    time = models.DateTimeField(default=django.utils.timezone.now)

class InterestInventoryTest(models.Model):
    question = models.CharField(max_length=500)



class InterestInventoryTestScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.CharField(max_length=100)
    time = models.DateTimeField(default=django.utils.timezone.now)



class LettersTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    test_type = models.CharField(max_length=10, choices=[("1", 'Pre Test'), ("2", "Post test")])
    time = models.DateTimeField(default=timezone.now)
    test_letters = models.CharField(max_length=500,default = None)
    answer_letters = models.CharField(max_length=500,default = None)
    time = models.DateTimeField(default=django.utils.timezone.now)

class SentencesTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentence1 = models.CharField(max_length=255,blank=True)
    sentence2 = models.CharField(max_length=255,blank=True)
    sentence3 = models.CharField(max_length=255,blank=True)
    sentence4 = models.CharField(max_length=255,blank=True)
    sentence5 = models.CharField(max_length=255,blank=True)
    time = models.DateTimeField(default=django.utils.timezone.now)

class ComprehensionsTest(models.Model):
    levels = [("Pre Primer", "Pre Primer"),
              ("Primer", "Primer"),
              ("Level 1", "Level 1"),
              ("Level 2", "Level 2"),
              ("Level 3", "Level 3"),
              ("Level 4", "Level 4"),
              ("Level 5", "Level 5"),
              ("Level 6", "Level 6")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=25, choices=levels, default=None)
    test_type = models.CharField(max_length=25, choices=[("Pre Test", "Pre Test"), ("Post Test", "Post Test")],default=None)
    story = models.CharField(max_length = 2000, default = None)
    spoken_story  = models.CharField(max_length = 2000, default = None)
    questions_list = models.CharField(max_length = 2000, default = None)
    answers_list = models.CharField(max_length = 2000, default = None)
    time = models.DateTimeField(default=django.utils.timezone.now)


class WordsTest(models.Model):
    levels = [("Pre Primer", "Pre Primer"),
              ("Primer", "Primer"),
              ("Level 1", "Level 1"),
              ("Level 2", "Level 2"),
              ("Level 3", "Level 3"),
              ("Level 4", "Level 4"),
              ("Level 5", "Level 5"),
              ("Level 6", "Level 6")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    words = models.CharField(max_length=500)
    spoken_words = models.CharField(max_length=500)
    level = models.CharField(max_length=20, choices=levels)
    test_type = models.CharField(max_length=10, choices=[("1", 'Pre Test'), ("2", "Post test")])
    time = models.DateTimeField(default=django.utils.timezone.now)










