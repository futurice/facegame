"""view for nameguessing gamemode"""
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from faceguessing.models import Player, UserStats
from faceguessing.views import __read_fum_user, get_all_names, check_usednames, random_user, hash_thumb
import random
import json
import hashlib
import os

def nameguessing(request):
    """render the template when user enters site"""
    player = Player.objects.get(playerid=request.user.username)
    return render_to_response('nameguessing.html',{'player': player}, context_instance=RequestContext(request, {}))

def get_thumbnail(request):
    """returns the thumbnail picture of given person"""
    player = Player.objects.get(playerid=request.user.username)
    choice = request.GET.get('choice', '')
    for random_user in get_all_names():
        if choice == hash_thumb(random_user):
            user = random_user
            break
    return HttpResponse(open(settings.PATH_TO_FUTUPIC + "thumbs/" + user + ".jpg").read(), content_type="image/jpg")

def json_thumbnails(request):
    """renders a new set of thumbnails to the game"""
    connected_user = request.user.username
    player, create = Player.objects.get_or_create(playerid=connected_user)
    if create:
        player.currentCorrectUser = ''
        player.currentRandomUsers = []
        player.usednames = [request.user.username]
        player.stats = {'correctAnswers': 0, 'wrongAnswers': 0, 'currentStreak': 0, 'highestStreak': 0, 'skips': 0}
        player.save()
    names = request.session.setdefault('names', get_all_names())

    randomusers, currentcorrect = random_user(player.usednames, names, player)
    player.currentRandomUsers = randomusers
    player.currentCorrectUser = currentcorrect
    player.save()

    user_dicts = [__read_fum_user(user) for user in player.currentRandomUsers]
    thumbnail_choices = [user['username'] for user in user_dicts]

    correct_dict = __read_fum_user(player.currentCorrectUser)
    correct_name_translated = "%s %s"%(correct_dict['first_name'], correct_dict['last_name'])

    image_hashes = []
    for user in player.currentRandomUsers:
        choice_hash = hash_thumb(user)
        image_hashes.append(choice_hash)
    player.save()
    json_thumbnails_render = render_to_string('thumbnails.html', {'thumbnail_choices': thumbnail_choices, 'player': player, 'image_hashes': image_hashes, 'correct_name_translated': correct_name_translated, 'random': random.randint(1, 10000000)}, context_instance=RequestContext(request, {}))
    player.save()
    return HttpResponse(json.dumps({'json_thumbnails': json_thumbnails_render}), content_type='application/json')

def check_hash(request):
    """checks the hash of the clicked image, to see if it's the correct or wrong answer"""
    connected_user = request.user.username
    player, create = Player.objects.get_or_create(playerid=connected_user)
    userstats, created = UserStats.objects.get_or_create(username=player.currentCorrectUser)
    correct_image_hash = hash_thumb(player.currentCorrectUser)

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
    return HttpResponse(json.dumps({'valid': valid, 'correctAnswers': correctAnswers, 'wrongAnswers': wrongAnswers, 'skips': skips, 'currentStreak': currentStreak, 'highestStreak': highestStreak }), content_type='application/json')


