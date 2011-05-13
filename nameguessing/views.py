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
from facegame.namegen.gen import get_random_name
from faceguessing.views import getAllNames, __read_fum_user
import random
import json
import hashlib
import os

def nameguessing(request):
	connected_user = "jsaa"
	player, create = Player.objects.get_or_create(playerid=connected_user)
	if create:
		print "player created"
		player.currentCorrectUser = ''
		player.currentRandomUsers = []
		player.usednames = [request.user.username]
		player.stats = {'correctAnswers': 0, 'wrongAnswers': 0, 'currentStreak': 0, 'highestStreak': 0, 'skips': 0}
		player.save()
	else:
		print "player not created"
		print player.playerid
	names = request.session.setdefault('names', getAllNames(connected_user))

	randomusers, currentcorrect = random_user(player.usednames, names, player)
	player.currentRandomUsers = randomusers
        player.currentCorrectUser = currentcorrect

	print player.currentCorrectUser
	print player.currentRandomUsers
	user_dicts = [__read_fum_user(user, connected_user) for user in player.currentRandomUsers]
	thumbnailChoices = [user['uid'] for user in user_dicts]
	print thumbnailChoices

	correct_dict = __read_fum_user(player.currentCorrectUser, connected_user)
	correct_name_translated = correct_dict['cn']

	image_hashes = []
	for user in player.currentRandomUsers:
		choice_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ user + ".jpg").read()).hexdigest()
		image_hashes.append(choice_hash)
	print image_hashes
	print hashlib.md5(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ player.currentCorrectUser + ".jpg").read()).hexdigest()
	print player.currentCorrectUser
	player.save()
	return render_to_response('nameguessing.html', {'thumbnailChoices': thumbnailChoices, 'player': player, 'image_hashes': image_hashes, 'correct_name_translated': correct_name_translated}, context_instance=RequestContext(request, {}))

def get_thumbnail(request):
	print "getting thumbnail"
	player = Player.objects.get(playerid="jsaa")
	thumbnailChoices = request.GET.get('choice', '')
	print thumbnailChoices
#	correctThumb = open(settings.PATH_TO_FUTUPIC +"thumbs/"+ player.currentCorrectUser + ".jpg").read()
#	randomThumbs = [correctThumb]
#	for item in player.currentRandomUsers:
#		randomThumbs.append(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ item + ".jpg").read())
#	random.shuffle(randomThumbs)
	return HttpResponse(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ thumbnailChoices + ".jpg").read(),content_type="image/jpg")

def json_thumbnails(request):
	print "creating new thumbnails in json"
	connected_user = "jsaa"
	player = Player.objects.get(playerid=connected_user)
	names = getAllNames(connected_user)

	randomusers, currentcorrect = random_user(player.usednames, names, player)
	player.currentRandomUsers = randomusers
        player.currentCorrectUser = currentcorrect

	user_dicts = [__read_fum_user(user, connected_user) for user in player.currentRandomUsers]
	thumbnailChoices = [user['uid'] for user in user_dicts]
	print thumbnailChoices

	correct_dict = __read_fum_user(player.currentCorrectUser, connected_user)
	correct_name_translated = correct_dict['cn']

	image_hashes = []
	for user in player.currentRandomUsers:
		choice_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ user + ".jpg").read()).hexdigest()
		image_hashes.append(choice_hash)

	json_thumbnails = render_to_string('thumbnails.html', {'thumbnailChoices': thumbnailChoices, 'player': player, 'image_hashes': image_hashes, 'correct_name_translated': correct_name_translated}, context_instance=RequestContext(request, {}))
	print "json thumbnails rendered"
	player.save()
	return HttpResponse(json.dumps({'json_thumbnails': json_thumbnails}), content_type='application/json')

def check_hash(request):
	print "updating stats"
	connected_user = "jsaa"
	player, create = Player.objects.get_or_create(playerid=connected_user)
	print player.currentCorrectUser
	userstats, created = UserStats.objects.get_or_create(username=player.currentCorrectUser)
	correct_image_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ player.currentCorrectUser + ".jpg").read()).hexdigest()

	print "is " + request.POST['answer'] + " same as " + correct_image_hash
	if request.POST['answer'] == correct_image_hash:
		print "yay you clicked the correct one"
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
		print "you clicked the wrong one :("
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
	print "randoming users thumbs"
	names_set = set(names)
	used_names_set = set(used_names)
	not_used = list(names_set - used_names_set)
	rncorrect = random.choice(not_used)
	while os.path.exists(settings.PATH_TO_FUTUPIC +""+ rncorrect + ".png") is False:
		print settings.PATH_TO_FUTUPIC +""+ rncorrect + ".png"
   		rncorrect = random.choice(not_used)

	for user in player.currentRandomUsers:
		rncorrect_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ user + ".jpg").read()).hexdigest()
		missing = os.path.exists(settings.PATH_TO_FUTUPIC +"thumbs/"+ user + ".jpg")
		while rncorrect_hash == settings.ANONYMOUS_THUMB or missing is False:
			rncorrect = random.choice(not_used)
			rncorrect_hash = hashlib.md5(open(settings.PATH_TO_FUTUPIC +"thumbs/"+ user + ".jpg").read()).hexdigest()
			missing = os.path.exists(settings.PATH_TO_FUTUPIC +"thumbs/"+ user + ".jpg")

	random_names = [rncorrect]
	for ind in range(0, 4):
		rn = names[random.randrange(0, len(names))]
		while rn in random_names:
			rn = names[random.randrange(0, len(names))]
		random_names.append(rn)
	random.shuffle(random_names)
	return random_names, rncorrect
