from django.http import JsonResponse
from rest_framework.response import  Response
from rest_framework.decorators import  api_view
from django.core import serializers
from .models import IntroTest, Letters, UserAccounts, Sentences, Words, Comprehensions, Questions,MultipleIntelligenceTest,InterestInventoryTest,LettersTest,SentencesTest, ComprehensionsTest, WordsTest, MultipleIntelligenceTestScore, InterestInventoryTestScore
from .serializers import  IntroSerializer,LettersSerializer,LetterScoreSerializer, SentencesSerializer,SentencesTestSerializer, WordsSerializer,WordsTestSerializer,ComprehensionsSerializer,ComprehensionsTestSerializer,MultipleIntelligenceTestScoreSerializer,InterestInventoryTestScoreSerializer
from django.http import HttpResponse
import random, difflib, string
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        ## This data variable will contain refresh and access tokens
        data = super().validate(attrs)
        ## You can add more User model's attributes like username,email etc. in the data dictionary like this.
        data['is_staff'] = self.user.is_staff
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def intro_validator(request,user_id):
    print('In validator')
    print(user_id)
    db_user_id = IntroTest.objects.filter(user = user_id).exists()
    print('our user id: ',db_user_id)
    if db_user_id:
        return JsonResponse({"found":True})
    else:
        return JsonResponse({"found":False})

def staff_validator(request,user_id):
    user = UserAccounts.objects.get(id = user_id)
    print(user)
    if user.is_staff:
        return JsonResponse({"is_staff":True})
    else:
        return JsonResponse({"is_staff":False})

@api_view(['POST'])
def intro_completed(request):
    intro_data = JSONParser().parse(request)
    data = IntroSerializer(data=intro_data)
    print(data)
    if data.is_valid():
        data.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        print('data not valid')
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_letters(request):
    letters = sorted(Letters.objects.all().order_by('letter'), key=lambda x: random.random())
    serializer = LettersSerializer(letters,many= True)
    letter_list = []
    for i in range(0,26):
        letter_list.append(serializer.data[i]['letter'])
    return Response(letter_list)


@api_view(['GET'])
def get_sentences(request):
    sentences = Sentences.objects.all()
    serializer = SentencesSerializer(sentences,many = True)
    print(serializer)
    print(serializer.data)
    sentence_list = []
    for i in range(0,5):
        sentence_list.append(serializer.data[i]['sentence'])
    return Response(sentence_list)

@api_view(['POST'])
@csrf_exempt
def letters_score(request):
    letters_data = JSONParser().parse(request)
    data = LetterScoreSerializer(data = letters_data)
    print(letters_data)
    print(data)
    if data.is_valid():
        data.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        print('data not valid')
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def sentences_results(request):
    sentences_read = JSONParser().parse(request)
    print(sentences_read)
    actual_sent = Sentences.objects.all()
    post_serializer = SentencesTestSerializer(data = sentences_read)
    get_serializer =  SentencesSerializer(actual_sent,many = True)
    sentence_list = []
    score_list = []
    sent_read_list = [sentences_read['sentence1'],sentences_read['sentence2'],sentences_read['sentence3'],sentences_read['sentence4'],sentences_read['sentence5'],]
    for i in range(0, 5):
        sentence_list.append(get_serializer.data[i]['sentence'])
        score_list.append(difflib.SequenceMatcher(a = get_serializer.data[i]['sentence'].translate(str.maketrans('', '', string.punctuation)).lower(), b = sent_read_list[i]).ratio()*100)
    if post_serializer.is_valid():
        post_serializer.save()
        return JsonResponse({"score":score_list,"sentences":sentence_list},status=status.HTTP_201_CREATED)
    else:
        print('data not valid')
        return Response(status=status.HTTP_400_BAD_REQUEST)

def get_level(num):
    if num == 0:
        return 'Pre Primer'
    elif num == 1:
        return "Primer"
    elif num == 2:
        return "Level 1"
    elif num == 3:
        return "Level 2"
    elif num == 4:
        return "Level 3"
    elif num == 5:
        return "Level 4"
    elif num == 6:
        return "Level 5"
    elif num == 7:
        return "Level 6"


@api_view(['GET'])
def get_words(request,level):
    level = get_level(int(level))
    # print('words',words[0])
    if level  == "Pre Primer" or level == "Primer":
        length = 10
    elif level == "Level 1" or level == 'Level 2' or level == 'Level 3':
        length = 15
    elif level == 'Level 4' or level == 'Level 5' or level == 'Level 6':
        length = 20
    words = sorted(Words.objects.filter(level=level).values('word'), key=lambda x: random.random())
    print(words)
    words_list = []
    for word in words:
        words_list.append(word['word'])
    print(words_list[:length])
    return Response(words_list[:length],status= status.HTTP_200_OK)

@api_view(['POST'])
@csrf_exempt
def words_results(request):
    data = JSONParser().parse(request)
    data['level'] = str(get_level(int(data['level'])))
    data['user'] = int(data['user'])
    data['test_type'] = int(data['test_type'])
    print(data)
    post_serializer = WordsTestSerializer(data=data)
    if post_serializer.is_valid():
        post_serializer.save()
        return Response(status= status.HTTP_201_CREATED)
    else:
        print('data not valid')
        return Response(status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_story(request,test_type,level):
    level = get_level(int(level))
    if test_type == 1:
        test_type = 'Pre Test'
    else: test_type = 'Post Test'
    story = Comprehensions.objects.filter(level = level, test_type = test_type)
    questions = Questions.objects.filter(comprehension = story.values()[0]['id'])
    print(questions)
    q_list = []
    for q in questions.values():
        q_list.append(q['questions'])
    serializer = ComprehensionsSerializer(story, many=True)
    # print(serializer)
    # print(serializer.data)
    return JsonResponse({1:serializer.data[0],2:q_list,})


def getAnswersScore(questions,spoken_answer):
    scores = []
    for i in range(len(questions)):
        print(spoken_answer[i])
        question = Questions.objects.filter(questions = questions[i]).values()[0]
        score1 = difflib.SequenceMatcher(a = question['answer'].translate(str.maketrans('', '', string.punctuation)).lower(), b = spoken_answer[i]).ratio()*100
        score2 = difflib.SequenceMatcher(a = question.get('answer2').lower(),b =spoken_answer[i] ).ratio()*100
        score3 = difflib.SequenceMatcher(a = question.get('answer3').lower(),b =spoken_answer[i] ).ratio()*100
        score4 = difflib.SequenceMatcher(a=question.get('answer4').lower(), b=spoken_answer[i]).ratio()*100
        s = [score1,score2,score3,score4]
        scores.append(max(s))
    return scores



@api_view(["POST"])
def story_results(request):
    data = JSONParser().parse(request)
    data['level'] = get_level(int(data['level']))
    if data['test_type'] == 1:
        test_type = 'Pre Test'
    else: test_type = 'Post Test'
    data['test_type'] = test_type
    data['spoken_story'] = data['spoken_story']
    data['story'] = data['story']
    serializer = ComprehensionsTestSerializer(data = data)
    score = difflib.SequenceMatcher(a = data['spoken_story'].translate(str.maketrans('', '', string.punctuation)).lower(), b = data['story'].replace("\r\n", "")).ratio()*100
    answers_scores = getAnswersScore(data['questions_list'].split(','),data['answers_list'].split(','))
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"1":score, "2":answers_scores},status = status.HTTP_201_CREATED, )
    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_multiple_inventory(request):
    options  = MultipleIntelligenceTest.objects.all().values()
    print(options)
    options_list = []
    for option in options:
        options_list.append(option['question'])

    return Response(options_list,status = status.HTTP_200_OK)



def compute_mi_score(answers,options):
    ans_dict = {"A":[],
                "B":[],
                "C":[],
                "D":[],
                "E":[],
                "F":[],
                "G":[]}
    for i in range(len(answers)):
        cat = MultipleIntelligenceTest.objects.filter(question = options[i]).values()[0]
        ans_dict[cat['type']].append(answers[i])

    return ans_dict


@api_view(["POST"])
@csrf_exempt
def multiple_inventory_results(request):
    data = JSONParser().parse(request)
    print(data['answers'])
    ans_groups = compute_mi_score(data['answers'],data['options'])
    print(ans_groups)
    new_data = {"user":data['user'],
                'linguistic':','.join(str(i) for i in ans_groups['A']),
                'logical_mathematical':','.join(str(i) for i in ans_groups['B']),
                'musical':','.join(str(i) for i in ans_groups['C']),
                'spatial':','.join(str(i) for i in ans_groups['D']),
                'bodily':','.join(str(i) for i in ans_groups['E']),
                'intra_personal':','.join(str(i) for i in ans_groups['F']),
                'inter_personal':','.join(str(i) for i in ans_groups['G'])}
    print(new_data)
    serializer = MultipleIntelligenceTestScoreSerializer(data = new_data)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response(ans_groups,status = status.HTTP_201_CREATED)
    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_interest_inventory(request):
    options = InterestInventoryTest.objects.all().values()
    print(options)
    options_list = []
    for option in options:
        options_list.append(option['question'])

    return Response(options_list, status=status.HTTP_200_OK)

@api_view(['POST'])
def interest_inventory_results(request):
    data = JSONParser().parse(request)
    data['score'] = ','.join(str(i) for i in data['score'])
    serializer = InterestInventoryTestScoreSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response(status = status.HTTP_201_CREATED)
    else: return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_users_list(request):
    users = UserAccounts.objects.filter(is_staff=False, is_admin = False,is_active=True).values('id','f_name','l_name','username','email','date_joined','last_login')
    return Response(users,status = status.HTTP_200_OK)


@api_view(['GET'])
def get_tests_list(request,user_id):
    letter_results = LettersTest.objects.filter(user_id = user_id).values()
    words_results = WordsTest.objects.filter(user_id = user_id).values()
    sentences_results = SentencesTest.objects.filter(user_id = user_id).values()
    story_results = ComprehensionsTest.objects.filter(user_id = user_id).values()
    mi_results =MultipleIntelligenceTestScore.objects.filter(user_id = user_id).values()
    ii_results = InterestInventoryTestScore.objects.filter(user_id = user_id).values()
    print(mi_results)
    return JsonResponse({"letter_results":list(letter_results),
                         "words_results":list(words_results),
                         "sentences_results":list(sentences_results),
                         "story_results":list(story_results),
                        "mi_results": list(mi_results),
                         "ii_results":list(ii_results)})




@api_view(['GET'])
def get_sentence_results(request,id,user_id):
    data = list(SentencesTest.objects.filter(id = id, user_id = user_id).values("sentence1","sentence2","sentence3","sentence4","sentence5"))
    sentences = list(Sentences.objects.all().values('sentence'))
    spoken = []
    for i in range(5):
        if i == 0:
            spoken.append(data[0]['sentence1'])
        elif i == 1:
            spoken.append(data[0]['sentence2'])
        elif i == 2:
            spoken.append(data[0]['sentence3'])
        elif i == 3:
            spoken.append(data[0]['sentence4'])
        elif i == 4:
            spoken.append(data[0]['sentence5'])
    final = []
    print(spoken)
    for i in range(5):

        if(sentences[i]['sentence'] == '' or spoken[i] == ''):
            score = 0
        else:
            score=difflib.SequenceMatcher(a = sentences[i]['sentence'].translate(str.maketrans('', '', string.punctuation)).lower(), b =spoken[i]).ratio()*100
        final.append([sentences[i]['sentence'], spoken[i],score])
    return Response(final,status = status.HTTP_200_OK)

@api_view(['GET'])
def get_letter_results(request,id,user_id):
    data = list(LettersTest.objects.filter(id = id, user_id = user_id).values())
    return Response(data,status=status.HTTP_200_OK)

@api_view(['GET'])
def get_story_results(request, id, user_id):
    data = list(ComprehensionsTest.objects.filter(id = id, user_id = user_id).values())
    data[0]['answers_score']=(getAnswersScore(data[0]['questions_list'].split(','),
                                data[0]['answers_list'].split(',')))
    data[0]['story'] = data[0]['story'].translate(str.maketrans('', '', string.punctuation))
    data[0]['story_score'] = difflib.SequenceMatcher(a=data[0]['story'].translate(str.maketrans('', '', string.punctuation)).lower(), b=data[0]['spoken_story'].replace("\r\n", " ")).ratio() * 100
    return Response(data)


@api_view(['GET'])
def get_words_results(request, id, user_id):
    data = list(WordsTest.objects.filter(id = id, user_id = user_id).values())

    return Response(data)


@api_view(['GET'])
def get_mi_results(request, id, user_id):
    data = list(MultipleIntelligenceTestScore.objects.filter(id = id, user_id = user_id).values())

    return Response(data)


@api_view(['GET'])
def get_ii_results(request, id, user_id):
    options = InterestInventoryTest.objects.all().values()
    print(options)
    options_list = []
    for option in options:
        options_list.append(option['question'])
    data = list(InterestInventoryTestScore.objects.filter(id = id, user_id = user_id).values())
    data[0]['options'] = options_list

    return Response(data)
