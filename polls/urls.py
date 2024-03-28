# polls 폴터에 urls.py 가 없어서 새로 생성
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), # cafe_menu -> views.py -> index함수로 이동
    path("menu", views.menu, name='etc'),
    path("order", views.order_coffee, name='coffee')
] 