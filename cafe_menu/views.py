from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the cafe_menu index.")

def menu(request): # 메뉴가 실행되면 
    return HttpResponse("우리집 맛집입니다.") # 우리집 맛집입니다. 출력

def order_coffee(request):
    return HttpResponse("커피 한잔!")