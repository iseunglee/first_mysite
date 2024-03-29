from django.http import HttpResponse, Http404
from .models import Question, Choice
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")
    total_questions = Question.objects.count()
    context = {'latest_question_list': latest_question_list, 'total_questions':total_questions}
    return render(request, 'polls/index.html', context)

# index1을 만들고, index1.html을 만들어서 하나 동작시켜보자

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

# question_id 말고 다른 이름으로 받아도 될까?
# 숫자가 아닌게 들어오면 어떻게 되지?
# 2개 다른 경로로 들어오고 question_id가 표시되는 view의 함수를 만들어봅시다.
def results_num(request, question_num):
    return HttpResponse(f"너는 {question_num}의 결과를 보고 있다.")

def vote_num(request, question_num):
    return HttpResponse(f"너는 {question_num}에 투표했다.")

# view + HttpResponse 연습문제
# 1. 
def recent_question(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:10]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

# 2.
def today_questions(request):
    today = timezone.now().date()
    questions_today = Question.objects.filter(pub_date__date=today)
    output = ", ".join([q.question_text for q in questions_today])
    return HttpResponse(output)

# 3.
def print_hello_world(request):
    return HttpResponse("Hello, world!")

# 4.
def this_year_question(request):
    this_year = timezone.now().year
    outputs = Question.objects.filter(pub_date__year=this_year)
    output = ", ".join([q.question_text for q in outputs])
    return HttpResponse(output)