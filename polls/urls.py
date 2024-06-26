# polls 폴터에 urls.py 가 없어서 새로 생성
from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    # ex: /polls/
    # path("", views.index, name="index"),
    path("", views.IndexView.as_view(), name="index"), 
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),

    path("<str:question_num>/results_num/", views.results_num, name='results_num'),

    path("<str:question_num>/vote_num/", views.vote_num, name="vote_num"),
    
    path("recent/", views.recent_question, name="recent_question"),

    path("today/", views.today_questions, name='today_questions'),

    path("hello/", views.print_hello_world, name="print_hello_world"),
    
    path("this_year/", views.this_year_question, name='this_year_question'),

    path('question/new/', views.QuestionCreateView.as_view(), name='question_new'),

    path('question/<int:pk>/choice/new/', views.ChoiceCreateView.as_view(), name='choice_new'),

    path('question/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),

    path('choice/<int:pk>/update/', views.ChoiceUpdateView.as_view(), name='choice_update'),

    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
] 