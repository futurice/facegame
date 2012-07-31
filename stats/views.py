from django.core.cache import cache
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from fumapi import read, read_list
from django import forms
from faceguessing.models import Player, UserStats
from faceguessing.views import __read_fum_user
import random
import json
import hashlib
import os
from operator import itemgetter

def hall_of_fame(request):
    try:
        player = UserStats.objects.get(username=request.user.username)
    except:
        player = None
    hall_of_fame_list = Player.objects.all()
#UserStats.objects.order_by('-success')
    hall_of_fame = []
    for item in hall_of_fame_list:
         if item.stats['highestStreak'] < 5:
             continue
         try:
             user = __read_fum_user(item.playerid, request.user.username)
         except:
             continue
         hall_of_fame.append({"highestStreak": item.stats["highestStreak"], "wrongAnswers": item.stats["wrongAnswers"], 'user': user})
#        player.stats = {'correctAnswers': 0, 'wrongAnswers': 0, 'currentStreak': 0, 'highestStreak': 0, 'skips': 0}
         
    hall_of_fame = sorted(hall_of_fame, key=itemgetter('highestStreak'))
    hall_of_fame.reverse()
    return render_to_response("hall_of_fame.html", {"player": player, 'hall_of_fame': hall_of_fame }, context_instance=RequestContext(request))

