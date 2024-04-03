from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    #pub_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField('pub date')
    # question_text 출력
    def __str__(self) -> str:
        return self.question_text + '_Question'
    
    # 어드민 페이지 커스터마이징, published 더 깔끔히 표현 잘 되도록
    @admin.display(
            boolean=True,
            ordering="pub_date",
            description="Published recently?"
    )
    # 최근에 만들어졌니
    # def was_published_recently(self):
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # question_text 길이 출력
    def load_question_text_length(self):
        return len(self.question_text)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text