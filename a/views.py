from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
import requests
import json
from datetime import datetime

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes


@login_required(login_url='/accounts/facebook/login')
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def callback(request):
    context = {}
    if "id" in request.GET:
        context["id"] = request.GET["id"]
    else:
        context["id"] = ""

    token = SocialToken.objects.get(account__user=request.user, account__provider='facebook')
    account = SocialAccount.objects.get(user=request.user)
    url = "https://graph.facebook.com/v2.6/{0}/events/attending?access_token={1}".format(
        account.uid,
        token,
    )
    params = {
    }
    response = requests.get(url, data=params)
    data = json.loads(response.text)
    all_events = data["data"]
    context["data"] = []
    for event in all_events:
        try:
            end = datetime.strptime(event["end_time"], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
            if end > datetime.now():
                event_dict = {
                    "start": event["start_time"],
                    "end": event["end_time"],
                    "summary": event["name"]
                }
                context["data"].append(event_dict)
        except KeyError:
            pass

    post_url = "http://www.aviato.space/api/facebook"
    print(requests.post(post_url, json=context).status_code)

    return Response(context)


def facebook_redirect(request):
    if "id" in request.GET:
        some_id = request.GET["id"]
    else:
        some_id = ""
    return HttpResponseRedirect('/callback?id={0}'.format(some_id))
