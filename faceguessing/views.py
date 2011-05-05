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
from models import Player
import random
import json
import hashlib
import os

class NameForm(forms.Form):
	name = forms.ChoiceField(widget = forms.RadioSelect)


def get_user_image(request):
    player = Player.objects.get(playerid=request.META['REMOTE_USER'])
    return HttpResponse(open("/var/www/intra.futurice.org/futupic/" + player.currentCorrectUser + ".png").read(),content_type="image/png")

def jsonform(request):
	print "creating a json form"
	player = Player.objects.get(playerid=request.META['REMOTE_USER'])
	names = getAllNames()
	form = createForm(request, player, names)
	jsonform = render_to_string('form.html', {'form': form, 'player': player, 'random': random.randint(1,10000000)}, context_instance=RequestContext(request, {}))
	print "json form rendered"
	return HttpResponse(json.dumps({'jsonform': jsonform}), content_type='application/json')

def updatestats(request):
	print "updating stats"
	player = Player.objects.get(playerid=request.META['REMOTE_USER'])
	if request.POST['answer'] == player.currentCorrectUser:
		player.stats['correctAnswers'] += 1
		player.stats['currentStreak'] += 1
         	player.usednames += [player.currentCorrectUser]
		if player.stats['highestStreak'] < player.stats['currentStreak']:
			player.stats['highestStreak'] += 1
		valid = True
	elif request.POST['answer'] == "SKIPSKIP":
		player.stats['skips'] += 1
		valid = True
	elif request.POST['answer'] == "RESET":
		player.stats = {'correctAnswers': 0, 'wrongAnswers': 0, 'currentStreak': 0, 'highestStreak': 0, 'skips': 0}
		valid = False
	else:
		player.stats['wrongAnswers'] += 1
		player.stats['currentStreak'] = 0
		valid = False
	correctAnswers = player.stats['correctAnswers']
	wrongAnswers = player.stats['wrongAnswers']
	skips = player.stats['skips']
	currentStreak = player.stats['currentStreak']
	highestStreak = player.stats['highestStreak']
	player.save()
	print "stats updated"
	return HttpResponse(json.dumps({'valid': valid, 'correctAnswers': correctAnswers, 'wrongAnswers': wrongAnswers, 'skips': skips, 'currentStreak': currentStreak, 'highestStreak': highestStreak }), content_type='application/json')

def index(request):
	player, create = Player.objects.get_or_create(playerid=request.META['REMOTE_USER'])
	if create:
		print "player created"
		player.currentCorrectUser = ''
		player.currentRandomUsers = []
		player.usednames = []
		player.stats = {'correctAnswers': 0, 'wrongAnswers': 0, 'currentStreak': 0, 'highestStreak': 0, 'skips': 0}
		player.save()
	else:
		print "player not created"
		print player.playerid
	names = request.session.setdefault('names', getAllNames())
	form = createForm(request, player, names)
	return render_to_response('template.html', {'form': form, 'player': player, 'random': random.randint(1,10000000)}, context_instance=RequestContext(request, {}))

def getAllNames():
	print "getting all names"
        names = cache.get("all-futurice-names")
        if names is None:
   	     names = [user['rdn_value'] for user in read('group', 'Futurice')['uniqueMember']]
             cache.set("all-futurice-names", names, 3600)
	return names

def createForm(request, player, names):
	print "creating a form"
	form = NameForm()
	unp = Paginator(player.usednames, 1)
	unc = unp.count
	if unc > 50:
		player.usednames = []
		player.save()
        randomusers, currentcorrect = random_user(player.usednames, names)
	player.currentRandomUsers = randomusers
        player.currentCorrectUser = currentcorrect
	player.save()
	createFormChoices(request, player, form)
	print "form created"
	return form

def __read_fum_user(user):
    user_details = cache.get("fum3-user-%s" % user)
    if user_details is None:
        user_details = read('user', user)
        cache.set("fum3-user-%s" % user, user_details, 3600)
    return user_details

def createFormChoices(request, player, form):
	print "creating form choices"
	user_dicts = [__read_fum_user(user) for user in player.currentRandomUsers]
	formchoices = [(user['uid'], user['cn']) for user in user_dicts]
	form.fields['name'].choices = formchoices
	request.session['choices'] = formchoices
	print "form choices created"

def random_user(used_names, names):
	names_set = set(names)
	used_names_set = set(used_names)
	not_used = list(names_set - used_names_set)
	rncorrect = random.choice(not_used)
#not_used[random.randrange(0, len(not_used))]
	while os.path.exists("/var/www/intra.futurice.org/futupic/" + rncorrect + ".png") == False:
   		rncorrect = random.choice(not_used)
	rncorrect_hash = hashlib.md5(open("/var/www/intra.futurice.org/futupic/" + rncorrect + ".png").read()).hexdigest()
        missing = os.path.exists("/var/www/intra.futurice.org/futupic/" + rncorrect + ".png")
	while rncorrect_hash == settings.ANONYMOUS_PIC or missing is False:
   		rncorrect = random.choice(not_used)
		rncorrect_hash = hashlib.md5(open("/var/www/intra.futurice.org/futupic/" + rncorrect + ".png").read()).hexdigest()
                missing = os.path.exists("/var/www/intra.futurice.org/futupic/" + rncorrect + ".png")

	random_names = [rncorrect]
	for ind in range(0, 4):
		rn = names[random.randrange(0, len(names))]
		while rn in random_names:
			rn = names[random.randrange(0, len(names))]
		random_names.append(rn)
	random.shuffle(random_names)
	return random_names, rncorrect
