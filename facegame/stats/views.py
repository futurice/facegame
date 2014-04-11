from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django import forms

from facegame.faceguessing.models import Player, UserStats
from facegame.faceguessing.views import get_user

import random
import json
import hashlib
import os
from operator import itemgetter

def hall_of_fame(request):
    try:
        player = UserStats.objects.get(user=request.user)
    except:
        player = None
    hall_of_fame_list = Player.objects.all()
    hall_of_fame = []
    for item in hall_of_fame_list:
        if item.stats['highestStreak'] < 5:
            continue
        if not item.username:
            continue
        try:
            user = get_user(item.username)
        except Exception, e:
            continue
        hall_of_fame.append({"highestStreak": item.stats["highestStreak"], "wrongAnswers": item.stats["wrongAnswers"], 'user': user})
    hall_of_fame = sorted(hall_of_fame, key=itemgetter('highestStreak'))
    hall_of_fame.reverse()
    return render_to_response("hall_of_fame.html", {"player": player, 'hall_of_fame': hall_of_fame }, context_instance=RequestContext(request))

