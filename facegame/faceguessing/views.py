from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.defaulttags import csrf_token

from models import Player, UserStats
from facegame.namegen.gen import get_random_name
from facegame.common.helpers import get_api, to_json

import random
import json
import hashlib
import os

class NameForm(forms.Form):
    """class for the form"""
    name = forms.ChoiceField(widget = forms.RadioSelect)

def get_user_image(request):
    data = {'image': get_user(request.user.username)['portrait_thumb_url']}
    return to_json(data)

def jsonform(request):
    """returns a new form in json"""
    player = request.user
    names = get_all_names()
    form = create_form(player, names)
    rand_choice = player.currentCorrectUser
    context = RequestContext(request, {
        'form': form,
        'player': player,
        'choice': get_user(rand_choice)['portrait_thumb_url'],
        'random': random.randint(1, 10000000),
        })
    jsonform_render = render_to_string('form.html', context_instance=context)
    return HttpResponse(json.dumps({'jsonform': jsonform_render}), content_type='application/json')

def updatestats(request):
    """updates stats when something is clicked, i.e. wrong or correct answer"""
    player = request.user
    userstats, created = UserStats.objects.get_or_create(user=player)
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
    player = request.user
    names = request.session.setdefault('names', get_all_names())
    form = create_form(player, names)
    rand_choice = player.currentCorrectUser
    return render(request, 'template.html', {
        'form': form,
        'player': player,
        'choice': get_user(rand_choice)['portrait_thumb_url'],
        })

def get_all_names():
    return [k['username'] for k in get_game_data()['users']]

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

def is_valid_username(name):
    return name in get_all_names()

def valid_usernames(l):
    rs = []
    for username in l:
        if is_valid_username(username):
            rs.append(username)
    return rs

def check_usednames(player):
    """checks if usednames are x high, and if so, resets them"""
    # 'usednames' might not contain valid users anymore
    for username in player.usednames:
        if not is_valid_username(username):
            player.usednames.pop(player.usednames.index(username))

    page = Paginator(player.usednames, 1)
    if page.count>75:
        player.usednames = [player.username]
        player.save()

def get_comparison_hash(name):
    return hashlib.md5(settings.THUMB_SALT + name).hexdigest()

GAME_DATA = None
def get_game_data():
    global GAME_DATA
    if GAME_DATA is None:
        data = {'users': []}
        users = get_users()
        for user in users:
            user['img_hash'] = get_comparison_hash(user['portrait_thumb_url'])
        data['users'] = users
        GAME_DATA = data
    return GAME_DATA

def get_users():
    """ Get users that have a thumbnail portrait of themselves """
    groups = ['Futurice', 'External']
    KEY = 'fum-users'
    result = cache.get(KEY)
    if result is None:
        usernames = []
        for group in groups:
            usernames += get_api().groups(group).get().get('users')
        usernames = list(set(usernames))
        result = []
        for username in usernames:
            user = get_api().users(username).get(fields='username,first_name,last_name,portrait_thumb_url')
            if 'thumb' in user.get('portrait_thumb_url'):
                result.append(user)
        cache.set(KEY, result)
    return result

def get_kilod(l, value, key='username'):
    """ get key in list of dictionaries """
    r = [k for k in l if k[key]==value]
    return r[0] if r else None

def get_user(username):
    return get_kilod(get_game_data()['users'], username, key='username')

def create_form_choices(player, form):
    """creates the choices of 5 names to the form"""
    user_dicts = [k for k in [get_user(user) for user in player.currentRandomUsers] if k]
    formchoices = [(user['username'], "%s %s"%(user['first_name'], user['last_name'])) for user in user_dicts]
    while len(formchoices) < 5:
        formchoices.append(get_random_name())
    random.shuffle(formchoices)
    form.fields['name'].choices = formchoices

def random_user(used_names, names, player, limit=5, iteration_limit=100):
    """gets a set of 4 random names and 1 correct name for the player"""
    check_usednames(player)
    names_set = set(valid_usernames(names))
    used_names_set = set(valid_usernames(used_names))
    not_used = list(names_set - used_names_set)

    rncorrect = random.choice(not_used)

    random_names = [rncorrect]
    iterations = 0
    while len(random_names)<limit and iterations<iteration_limit:
        rn = names[random.randrange(0, len(names))]
        if rn and not (rn in random_names or rn in player.usednames):
            random_names.append(rn)
        iterations += 1
    random.shuffle(random_names)
    return random_names, rncorrect

def hash_thumb(username):
    return (get_user(username) or {}).get('img_hash', None)
