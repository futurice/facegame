from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render

from facegame.faceguessing.models import Player, UserStats
from facegame.faceguessing.views import get_user, get_all_names, check_usednames, random_user, hash_thumb, get_kilod, get_game_data
from facegame.common.helpers import to_json

import random
import json
import hashlib
import os

def nameguessing(request):
    player = request.user
    return render(request, 'nameguessing.html', {'player': player})

def get_image_for_hash(path):
    chosen_user = get_kilod(get_game_data()['users'], path, key='img_hash')
    data = None
    if chosen_user:
        data = chosen_user['portrait_thumb_url']
    return data

def get_thumbnail(request):
    """returns the thumbnail picture of given person by hash, or default to request.user """
    choice = request.GET.get('choice', get_user(request.user.username)['img_hash'])
    data = {}
    img = get_image_for_hash(choice)
    if img:
        data = {'image': img}
    return HttpResponse(to_json(data))

def json_thumbnails(request):
    """renders a new set of thumbnails to the game"""
    player = request.user
    names = request.session.setdefault('names', get_all_names())

    randomusers, currentcorrect = random_user(player.usednames, names, player)
    player.currentRandomUsers = randomusers
    player.currentCorrectUser = currentcorrect
    player.save()

    user_dicts = [k for k in [get_user(user) for user in player.currentRandomUsers] if k]
    thumbnail_choices = [user['username'] for user in user_dicts]

    correct_dict = get_user(player.currentCorrectUser)
    correct_name_translated = "%s %s"%(correct_dict['first_name'], correct_dict['last_name'])

    image_hashes = []
    for user in player.currentRandomUsers:
        choice_hash = hash_thumb(user)
        if choice_hash:
            image_hashes.append(choice_hash)
    player.save()

    context = RequestContext(request, {'thumbnail_choices': thumbnail_choices, 'player': player, 'image_hashes': image_hashes, 'correct_name_translated': correct_name_translated, 'random': random.randint(1, 10000000)})
    json_thumbnails_render = render_to_string('thumbnails.html', context_instance=context)
    player.save()
    return HttpResponse(json.dumps({'json_thumbnails': json_thumbnails_render}), content_type='application/json')

def check_hash(request):
    """checks the hash of the clicked image, to see if it's the correct or wrong answer"""
    player = request.user
    userstats, created = UserStats.objects.get_or_create(user=player)
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


