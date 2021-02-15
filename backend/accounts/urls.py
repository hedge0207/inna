from django.urls import path
from . import views

urlpatterns = [
    path('login/kakao', views.kakao_login),
    path('login/kakao/callback', views.kakao_callback),
]
