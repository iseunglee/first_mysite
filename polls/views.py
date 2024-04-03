from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse
from django.db.models import F
from django.views import generic # 제네릭 뷰를 위한
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Question


# 뷰 개선 수업내용
from django.utils import timezone


# DeleteView
class QuestionDeleteView(generic.edit.DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete.html'
    success_url = reverse_lazy('polls:index')  # 삭제 후 리다이렉션될 URL, 실제 프로젝트에 맞게 수정 필요

# UpdateView 연습문제
class ChoiceUpdateView(generic.edit.UpdateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_update_form.html'  # 재사용하거나 적절한 템플릿 지정

    def get_success_url(self):
        # 선택지가 업데이트된 후, 선택지가 속한 질문의 상세 페이지로 리다이렉션
        choice = self.object
        return reverse('polls:detail', kwargs={'question_id': choice.question.pk})


    # def get_success_url(self):
    #     return reverse('polls:detail', kwargs={'question_id': self.kwargs['pk']})

# UpdateView
class QuestionUpdateView(generic.edit.UpdateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/question_update_form.html'  # 재사용하거나 적절한 템플릿 지정
    success_url = reverse_lazy('polls:index')  # 예시 URL, 실제 프로젝트에 맞게 수정 필요

# CreateView
class QuestionCreateView(generic.edit.CreateView): # CreateView 는 generic.edit 안에 있다.
    model = Question # 생성할 모델 인스턴스의 클래스 지정
    fields = ['question_text', 'pub_date'] # 폼에 포함될 모델 필드를 지정 , 지정된 필드를 포함하는 모델 폼을 자동으로 생성
    template_name = 'polls/question_form.html' # 뷰에서 사용할 템플릿의 이름 지정
    success_url = reverse_lazy('polls:index')  # 객체 생성 후 리다이렉션될 URL 지정, reverse_lazy함수를 사용하여 지정하는 것이 일반적

# CreateView 연습문제
class ChoiceCreateView(generic.edit.CreateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_form.html'
    success_url = reverse_lazy('polls:index')

    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)


# IndexView
class IndexView(generic.ListView): # 제네릭 뷰를 위한 상속받기 
    # 연습문제 1. 가장 최근에 받은 질문
    template_name = "polls/index.html" # 경로
    context_object_name = "latest_question_list" # context 키 이름

    # def get_queryset(self): # 실제 값을 처리하는 메서드
    #     """Return the last five published questions."""
    #     return Question.objects.order_by("-pub_date")[:5]
    
    # 뷰 개선 수업내용
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5] # 뷰 개선을 통해 장고에서 만든 에러 확인

    # 연습 문제 2. 가장 투표를 많이 받은 질문
    # template_name = 'polls/index.html'
    # context_object_name = 'latest_question_list' # html 바꾸지 않기 위해 동일한 컨텍스트 이름 설정, 내용은 가장 투표를 많이 받은 질문

    # def get_queryset(self):
    #     """가장 많은 투표를 받은 질문"""
    #     output = Question.objects.annotate(total_votes=Sum('choice__votes')).order_by('-total_votes')[:1]
    #     return output

    # 연습 문제 3. 아직 투표가 없는 질문
    # template_name = 'polls/index.html'
    # context_object_name = 'latest_question_list'

    # def get_queryset(self):
    #     output = Question.objects.annotate(total_votes=Sum('choice__votes')).filter(total_votes=0)
    #     return output
    
    # 강사님쿼리
    # template_name = "polls/index.html" # 경로
    # context_object_name = "latest_question_list" # context 키 이름

    # def get_queryset(self): # 실제 값을 처리하는 메서드
    #     """Return the last five published questions."""
    #     qs = Question.objects.all()
    #     return sorted(qs, key = lambda q : sum([c.votes for c in q.choice_set.all()]), reverse=True)

# DetailView
class DetailView(generic.DetailView):
    model = Question
    # template_name = "polls/detail.html" # template_name 변경하지 않고 question_detail.html 생성해서 연결, [app_name]/[model_name]_detail.html

    # def get_object(self):
    #     question_id = self.kwargs['question_id']
    #     question = get_object_or_404(Question, pk=question_id)
    #     return question
    
    # 디테일 뷰 테스트를 위한 추가 메서드, 디테일뷰는 기본적으로 하나의 객체를 가져와야하지만, 여기선 get_queryset을 사용했다.
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# ResultsView
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    # 테스트 연습문제
    def get_object(self):
        """
        Excludes questions that don't have at least one choice.
        """
        # super().get_object() 대신 get_object_or_404를 사용하여 객체를 가져옵니다.
        # question의 choice가 없으면 페이지 나타내지 않는다
        obj = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        if not obj.choice_set.exists():
            raise Http404("No choices found for this question.")
        return obj

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")
    total_questions = Question.objects.count()
    context = {'latest_question_list': latest_question_list, 'total_questions':total_questions}
    return render(request, 'polls/index.html', context)

# index1을 만들고, index1.html을 만들어서 하나 동작시켜보자

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # choice_count = len(question.choice_set.all())
    # content_1 = question.choice_set.all()[0]
    question_list = Question.objects.all()
    context = {
         "question" : question,
         "question_list" : question_list,
    

    }
    return render(request, "polls/detail.html", context)

def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    # choice 데이터에서 해당하는 값에 votes를 +1
    #c = Choice.objects.get(pk=8)
    #c.votes += 1
    #c.save()
    #return HttpResponse("You're voting on question %s." % question_id)

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