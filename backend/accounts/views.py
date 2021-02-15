from django.shortcuts import redirect
import urllib

# Create your views here.


def kakao_login(request):
    app_rest_api_key = '23f3a5b585c741f74db74187f6b6ed81'
    redirect_uri = "http://127.0.0.1:8000/accounts/login/kakao/callback"
    return redirect(
        "https://kauth.kakao.com/oauth/authorize?client_id={}&redirect_uri={}&response_type=code".format(
            app_rest_api_key, redirect_uri)
    )


def kakao_callback(request):
    params = urllib.parse.urlencode(request.GET)
    return redirect('http://127.0.0.1:8000/accounts/login/kakao/callback?{}'.format(params))
