import requests
import os
import json
from django.shortcuts import redirect
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'secrets.json'), 'rb') as secret_file:
    secrets = json.load(secret_file)

BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback'


class GooGleException(Exception):
    pass


def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = secrets["GOOGLE"]["CLIENT_ID"]
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    try:
        client_id = secrets["GOOGLE"]["CLIENT_ID"]
        client_secret = secrets["GOOGLE"]["CLIENT_SECRET"]
        code = request.GET.get('code')
        """
        Access Token Request
        """
        token_request = requests.post(
            f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}")
        token_request_json = token_request.json()
        print(token_request_json)
        error = token_request_json.get("error")
        if error is not None:
            return GooGleException()
        access_token = token_request_json.get('access_token')
        """
        Login Request
        """
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        print(accept)
        accept_json = accept.json()
        error = accept_json.get("error")
        if error is not None:
            return GooGleException()
        return JsonResponse(accept_json)
    except GooGleException:
        return redirect('/error')


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
