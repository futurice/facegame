"""view for the faceguessing game"""
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django import forms
from django.contrib.auth.decorators import login_required

from models import Player, UserStats
from facegame.namegen.gen import get_random_name

import random
import json
import hashlib
import os

class NameForm(forms.Form):
    """class for the form"""
    name = forms.ChoiceField(widget = forms.RadioSelect)

def get_user_image(request):
    """gets the image for the requested user"""
    player = Player.objects.get(playerid=request.user.username)
    return HttpResponse(open(settings.PATH_TO_FUTUPIC + "" + player.currentCorrectUser + ".png").read(), content_type="image/png")

def jsonform(request):
    """returns a new form in json"""
    connected_user = request.user.username
    player = Player.objects.get(playerid=connected_user)
    names = get_all_names()
    form = create_form(player, names)
    jsonform_render = render_to_string('form.html', {'form': form, 'player': player, 'random': random.randint(1, 10000000)}, context_instance=RequestContext(request, {}))
    return HttpResponse(json.dumps({'jsonform': jsonform_render}), content_type='application/json')

def updatestats(request):
    """updates stats when something is clicked, i.e. wrong or correct answer"""
    player = Player.objects.get(playerid=request.user.username)
    userstats, created = UserStats.objects.get_or_create(username=player.currentCorrectUser)
    if request.POST['answer'] == player.currentCorrectUser:
        userstats.success += 1
        if player.first_attempt:
            player.first_attempt = True
            userstats.first_success += 1
        player.stats['correctAnswers'] += 1
        player.stats['currentStreak'] += 1
        player.usednames += [player.currentCorrectUser]
        if player.stats['highestStreak'] < player.stats['currentStreak']:
            player.stats['highestStreak'] += 1
        valid = True
    elif request.POST['answer'] == "RESET":
        player.stats = {'correctAnswers': 0, 'wrongAnswers': 0, 'currentStreak': 0, 'highestStreak': 0, 'skips': 0}
        player.usednames = [request.user.username]
        valid = False
    else:
        player.stats['wrongAnswers'] += 1
        player.stats['currentStreak'] = 0
        userstats.failed_attempts += 1
        if player.first_attempt:
            player.first_attempt = False
            userstats.failed += 1
        valid = False
    correctAnswers = player.stats['correctAnswers']
    wrongAnswers = player.stats['wrongAnswers']
    skips = player.stats['skips']
    currentStreak = player.stats['currentStreak']
    highestStreak = player.stats['highestStreak']
    player.save()
    userstats.save()
    return HttpResponse(json.dumps({'valid': valid, 'correctAnswers': correctAnswers, 'wrongAnswers': wrongAnswers, 'skips': skips, 'currentStreak': currentStreak, 'highestStreak': highestStreak }), content_type='application/json')

def index(request):
    """render the game when player enters first time"""
    connected_user = request.user.username
    player, create = Player.objects.get_or_create(playerid=connected_user)
    if create:
        player.currentCorrectUser = ''
        player.currentRandomUsers = []
        player.usednames = [request.user.username]
        player.stats = {'correctAnswers': 0, 'wrongAnswers': 0, 'currentStreak': 0, 'highestStreak': 0, 'skips': 0}
        player.save()
    names = request.session.setdefault('names', get_all_names())
    form = create_form(player, names)
    import pdb; pdb.set_trace()
    return render_to_response('template.html', {'form': form, 'player': player, 'random': random.randint(1, 10000000)}, context_instance=RequestContext(request, {}))

def get_all_names():
    """gets the names of every Futurice employee"""
    usernames = cache.get("all-futurice-usernames")
    if usernames is None:
        usernames = settings.API.groups("Futurice").get()['users']
        cache.set("all-futurice-usernames", usernames, 3600)
    return usernames

def create_form(player, names):
    """creates the form with names"""
    form = NameForm()
    randomusers, currentcorrect = random_user(player.usednames, names, player)
    player.currentRandomUsers = randomusers
    player.currentCorrectUser = currentcorrect
    player.first_attempt = True
    player.save()
    create_form_choices(player, form)
    return form

def check_usednames(player):
    """checks if usednames are x high, and if so, resets them"""
    unp = Paginator(player.usednames, 1)
    unc = unp.count
    if unc > 75:
        player.usednames = [player.playerid]
        player.save()

def __read_fum_user(user):
    """reads user details (such as full name) from cache"""
    user_details = cache.get("fum5-user-%s" % user)
    if user_details is None:
        user_details = settings.API.users(user).get()
        cache.set("fum5-user-%s" % user, user_details, 10000)
    return user_details

def create_form_choices(player, form):
    """creates the choices of 5 names to the form"""
    user_dicts = [__read_fum_user(user) for user in player.currentRandomUsers]
    formchoices = [(user['username'], "%s %s"%(user['first_name'], user['last_name'])) for user in user_dicts]
    while len(formchoices) < 5:
        formchoices.append(get_random_name())
    random.shuffle(formchoices)
    form.fields['name'].choices = formchoices

def random_user(used_names, names, player):
    """gets a set of 4 random names and 1 correct name for the player"""
    check_usednames(player)
    names_set = set(names)
    used_names_set = set(used_names)
    not_used = list(names_set - used_names_set)
    
    rncorrect = False
    rncorrect_hash = None
    while not rncorrect or not os.path.exists(settings.PATH_TO_FUTUPIC + "thumbs/" + rncorrect + ".jpg") or rncorrect_hash == settings.ANONYMOUS_THUMB:
        rncorrect = random.choice(not_used)
    rncorrect_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC + "thumbs/" + rncorrect + ".jpg").read()).hexdigest()

    random_names = [rncorrect]
    for ind in range(0, 4):
        rn = ""
        rn_hash = ""
        while rn in random_names or rn in player.usednames or rn_hash == settings.ANONYMOUS_THUMB or not os.path.exists(settings.PATH_TO_FUTUPIC + "thumbs/" + rn + ".jpg"):
            rn = names[random.randrange(0, len(names))]
        rn_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC + "thumbs/" + rn + ".jpg").read()).hexdigest()
        random_names.append(rn)
    random.shuffle(random_names)
    return random_names, rncorrect

def hash_thumb(username):
    if os.path.exists(settings.PATH_TO_FUTUPIC + "thumbs/" + username + ".jpg"):
        return hashlib.md5(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ username + ".jpg").read()).hexdigest()
    return None
