"""view for nameguessing gamemode"""
#from django.core.cache import cache
#from django.core.context_processors import csrf
#from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
#from fumapi import read, read_list
#from django import forms
from faceguessing.models import Player, UserStats
#from facegame.namegen.gen import get_random_name
from faceguessing.views import __read_fum_user, get_all_names
import random
import json
import hashlib
import os

def nameguessing(request):
    """render the template when user enters site"""
    connected_user = "jsaa" #request.user.username
    player, create = Player.objects.get_or_create(playerid=connected_user)
    if create:
        player.currentCorrectUser = ''
        player.currentRandomUsers = []
        player.usednames = [request.user.username]
        player.stats = {'correctAnswers': 0, 'wrongAnswers': 0, 'currentStreak': 0, 'highestStreak': 0, 'skips': 0}
        player.save()
    names = request.session.setdefault('names', get_all_names(connected_user))

    randomusers, currentcorrect = random_user(player.usednames, names, player)
    player.currentRandomUsers = randomusers
    player.currentCorrectUser = currentcorrect
    player.save()

    user_dicts = [__read_fum_user(user, connected_user) for user in player.currentRandomUsers]
    thumbnail_choices = [user['uid'] for user in user_dicts]

    correct_dict = __read_fum_user(player.currentCorrectUser, connected_user)
    correct_name_translated = correct_dict['cn']

    image_hashes = []
    for user in player.currentRandomUsers:
        choice_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ user + ".jpg").read()).hexdigest()
        image_hashes.append(choice_hash)
    player.save()
    return render_to_response('nameguessing.html', {'thumbnail_choices': thumbnail_choices, 'player': player, 'image_hashes': image_hashes, 'correct_name_translated': correct_name_translated, 'random': random.randint(1, 10000000)}, context_instance=RequestContext(request, {}))

def get_thumbnail(request):
    """returns the thumbnail picture of given person"""
    print "getting thumbnail"
    player = Player.objects.get(playerid="jsaa")
    choice = request.GET.get('choice', '')
    for random_user in player.currentRandomUsers:
        if choice == hashlib.md5(open(settings.PATH_TO_FUTUPIC + "thumbs/" + random_user + ".jpg").read()).hexdigest():
            user = random_user
            break
    return HttpResponse(open(settings.PATH_TO_FUTUPIC + "thumbs/" + user + ".jpg").read(), content_type="image/jpg")

def json_thumbnails(request):
    """renders a new set of thumbnails to the game"""
    print "creating new thumbnails in json"
    connected_user = "jsaa" #request.user.username
    player = Player.objects.get(playerid=connected_user)
    names = get_all_names(connected_user)

    randomusers, currentcorrect = random_user(player.usednames, names, player)
    player.currentRandomUsers = randomusers
    player.currentCorrectUser = currentcorrect
    player.save()

    user_dicts = [__read_fum_user(user, connected_user) for user in player.currentRandomUsers]
    thumbnail_choices = [user['uid'] for user in user_dicts]
    print thumbnail_choices

    correct_dict = __read_fum_user(player.currentCorrectUser, connected_user)
    correct_name_translated = correct_dict['cn']

    image_hashes = []
    for user in player.currentRandomUsers:
        choice_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ user + ".jpg").read()).hexdigest()
        image_hashes.append(choice_hash)

    json_thumbnails_render = render_to_string('thumbnails.html', {'thumbnail_choices': thumbnail_choices, 'player': player, 'image_hashes': image_hashes, 'correct_name_translated': correct_name_translated, 'random': random.randint(1, 10000000)}, context_instance=RequestContext(request, {}))
    print "json thumbnails rendered"
    player.save()
    return HttpResponse(json.dumps({'json_thumbnails': json_thumbnails_render}), content_type='application/json')

def check_hash(request):
    """checks the hash of the clicked image, to see if it's the correct or wrong answer"""
    print "updating stats"
    connected_user = "jsaa" #request.user.username
    player, create = Player.objects.get_or_create(playerid=connected_user)
    userstats, created = UserStats.objects.get_or_create(username=player.currentCorrectUser)
    correct_image_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ player.currentCorrectUser + ".jpg").read()).hexdigest()

    if request.POST['answer'] == correct_image_hash:
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
    print "stats updated"
    return HttpResponse(json.dumps({'valid': valid, 'correctAnswers': correctAnswers, 'wrongAnswers': wrongAnswers, 'skips': skips, 'currentStreak': currentStreak, 'highestStreak': highestStreak }), content_type='application/json')

def random_user(used_names, names, player):
    """gets a set of 4 random names and 1 correct name for the player"""
    print "randoming users thumbs"
    names_set = set(names)
    used_names_set = set(used_names)
    not_used = list(names_set - used_names_set)
    rncorrect = random.choice(not_used)

    rncorrect_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC + "thumbs/" + rncorrect + ".jpg").read()).hexdigest()
    missing = os.path.exists(settings.PATH_TO_FUTUPIC + "thumbs/" + rncorrect + ".jpg")
    while rncorrect_hash == settings.ANONYMOUS_THUMB or missing is False:
        rncorrect = random.choice(not_used)
        rncorrect_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC + "thumbs/" + rncorrect + ".jpg").read()).hexdigest()
        missing = os.path.exists(settings.PATH_TO_FUTUPIC + "thumbs/" + rncorrect + ".jpg")

    random_names = [rncorrect]
    for ind in range(0, 4):
        rn = names[random.randrange(0, len(names))]
        rn_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC + "thumbs/" + rn + ".jpg").read()).hexdigest()
        while rn in random_names or rn in player.usednames or rn_hash == settings.ANONYMOUS_THUMB or os.path.exists(settings.PATH_TO_FUTUPIC + "thumbs/" + rn + ".jpg") is False:
            rn = names[random.randrange(0, len(names))]
            rn_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC + "thumbs/" + rn + ".jpg").read()).hexdigest()
        random_names.append(rn)
    random.shuffle(random_names)
    return random_names, rncorrect
