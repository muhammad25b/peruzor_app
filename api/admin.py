from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from .models import UserAccounts, Letters,LettersTest, Words, Sentences, Comprehensions, Questions, MultipleIntelligenceTest, InterestInventoryTest, IntroTest,ComprehensionsTest


# class UserAccountsConfig(UserAccounts):
#     list_display = ('email', 'username', 'is_staff', 'is_admin', 'is_active')

class UserAccountsConfig(UserAdmin):
    model = UserAccounts
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username', 'f_name','l_name', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'username', 'f_name','l_name',
                    'is_active', 'is_staff','is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'username','f_name','l_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'f_name','l_name', 'password1', 'password2', 'is_active', 'is_staff','is_superuser')}
         ),
    )


class LettersConfig(admin.ModelAdmin):
    model = Letters
    list_display = ('id', 'letter')
    ordering = ('id',)

class SentenceConfig(admin.ModelAdmin):
    model = Sentences
    list_display = ('id', 'sentence')
    ordering = ('id',)

class WordsConfig(admin.ModelAdmin):
    model = Words
    list_display = ('id', 'word','level')
    ordering = ('id',)

class StoryConfig(admin.ModelAdmin):
    model = Comprehensions
    list_display = ('id', 'title','story','level','test_type')
    ordering = ('id',)

class QuestionsConfig(admin.ModelAdmin):
    model = Questions
    list_display = ('id', 'questions','answer','comprehension')
    ordering = ('id',)

admin.site.register(UserAccounts,UserAccountsConfig)
admin.site.register(Letters,LettersConfig)
admin.site.register(Words,WordsConfig)
admin.site.register(Sentences, SentenceConfig)
admin.site.register(Comprehensions,StoryConfig)
admin.site.register(Questions,QuestionsConfig)
admin.site.register(MultipleIntelligenceTest)
admin.site.register(InterestInventoryTest)
admin.site.register(IntroTest)
admin.site.register(LettersTest)
admin.site.register(ComprehensionsTest)