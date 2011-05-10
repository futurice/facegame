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


def hall_of_fame(request):
    try:
        player = UserStats.objects.get(username=request.user.username)
    except:
        player = None
    hall_of_fame_list = UserStats.objects.order_by('-success')
    hall_of_fame = []
    for item in hall_of_fame_list:
         user = __read_fum_user(item.username, request.user.username)
         hall_of_fame.append({'stats': item, 'user': user})
    return render_to_response("hall_of_fame.html", {"player": player, 'hall_of_fame': hall_of_fame }, context_instance=RequestContext(request))

