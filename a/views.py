from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from allauth.socialaccount.models import SocialToken, SocialAccount
from allauth.socialaccount.forms import SignupForm
import requests
import json
from datetime import datetime


@login_required
def callback(request):
    token = SocialToken.objects.get(account__user=request.user, account__provider='facebook')
    account = SocialAccount.objects.get(user=request.user)
    url = "https://graph.facebook.com/v2.6/{0}/events/attending?access_token={1}".format(
        account.uid,
        token,
    )
    params = {
    }
    response = requests.get(url, data=params)
    print(account.uid)
    print(token)
    print(response)
    print(response.headers)
    print(response.text)
    data = json.loads(response.text)
    all_events = data["data"]
    valid_events = []
    for event in all_events:
        try:
            event_date = datetime.strptime(event["end_time"], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
            if event_date > datetime.now():
                valid_events.append(event)
        except KeyError:
            pass
    return HttpResponse("{0} events recorded, {1} of which are valid".format(len(all_events), len(valid_events)))


def facebook_redirect(request):
    return HttpResponseRedirect('/accounts/facebook/login/?process=login')


def cian(request):
    context = {
    }
    return render(request, "socialaccount/signup.html", context)
