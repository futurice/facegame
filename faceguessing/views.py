from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from fumapi import read, read_list
from django import forms
from models import Player
import random
import json

class NameForm(forms.Form):
	name = forms.ChoiceField(widget = forms.RadioSelect)

def jsonform(request):
	print "creating a json form"
	player = Player.objects.get(playerid="jsaa")
	if 'names' not in request.session:
		request.session['names'] = getAllNames()
	names = request.session['names']
	form = createForm(request, player, names)
	jsonform = render_to_string('form.html', {'form': form, 'player': player}, context_instance=RequestContext(request, {}))
	print "json form rendered"
	return HttpResponse(json.dumps({'jsonform': jsonform}), content_type='application/json')

def updatestats(request):
	print "updating stats"
	player = Player.objects.get(playerid="jsaa")
	if request.POST['answer'] == player.currentCorrectUser:
		player.stats['correctAnswers'] += 1
		player.stats['currentStreak'] += 1
		if player.stats['highestStreak'] < player.stats['currentStreak']:
			player.stats['highestStreak'] += 1
		valid = True
	elif request.POST['answer'] == "SKIPSKIP":
		player.stats['skips'] += 1
		valid = True
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
	return HttpResponse(json.dumps({'valid': valid, 'correctAnswers': correctAnswers, 'wrongAnswers': wrongAnswers, 'skips': skips, 'currentStreak': currentStreak, 'highestStreak': highestStreak}), content_type='application/json')

def index(request):
	player, create = Player.objects.get_or_create(playerid="jsaa")
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
#	if request.method == 'POST':
#		print "posted"
#		print player.usednames
#		print player.currentCorrectUser
#		print player.currentRandomUsers
#		#session = dict(request.session)
#		#random_users, correct_user = request.session['namesession']
#		#random_users = player.currentRandomUsers
#		#correct_user = player.currentCorrectUser
#		form = NameForm(request.POST, initial={'name': player.currentRandomUsers})
#		if 'choices' not in request.session:
#			print "choices not in session"
#			form.fields['name'].choices = [(user, read('user', user)['cn']) for user in player.currentRandomUsers]
#			print "form has choices now"
#		else:
#			print "choices were in session"
#			formchoices = request.session['choices']
#			form.fields['name'].choices = formchoices
#		print "pip"
#		if player.currentCorrectUser == request.POST['name']:
#			print "was correct user"
#			if form.is_valid():
#				print "is valid"
#				form = NameForm()
#				#request.session.pop('namesession', None)
#				#used_names = request.session.setdefault('used_names', [])
#				#used_names = player.usednames
#				player.currentRandomUsers, player.currentCorrectUser = random_user(player.usednames, names)
#				#used_names.append(correct_user)
#				player.usednames += [player.currentCorrectUser]
#				createFormChoices(request, player, form)
#				#request.session['namesession'] = random_users, correct_user
#				#request.session['used_names'] = used_names
#				#{'rnCorrect': correct_user}
#				player.save()
#				return render_to_response('form.html', {'form': form, 'rncorrect': player.currentCorrectUser}, context_instance=RequestContext(request))
#			else:
#				print "form was not valid"
#		else:
#			print "invalid name was posted, probably because the correct one was posted twice"
	#form = NameForm()
	#used_names = []
	#request.session['used_names'] = used_names
	form = createForm(request, player, names)
	#player.currentRandomUsers, player.currentCorrectUser = random_user(player.usednames, names)
	#player.usednames += [player.currentCorrectUser]
	#createFormChoices(request, player, form)
	#request.session['namesession'] = random_users, correct_user
	#request.session['used_names'] = used_names
	return render_to_response('template.html', {'form': form, 'player': player}, context_instance=RequestContext(request, {}))

def getAllNames():
	print "getting all names"
	names =  [user['rdn_value'] for user in read('group', 'Futurice')['uniqueMember']]
	return names

def createForm(request, player, names):
	print "creating a form"
	form = NameForm()
	player.currentRandomUsers, player.currentCorrectUser = random_user(player.usednames, names)
	player.usednames += [player.currentCorrectUser]
	player.save()
	createFormChoices(request, player, form)
	print "form created"
	return form

def createFormChoices(request, player, form):
	print "creating form choices"
	user_dicts = [read('user', user) for user in player.currentRandomUsers]
	formchoices = [(user['uid'], user['cn']) for user in user_dicts]
	#formchoices = [(user, read('user', user)['cn']) for user in player.currentRandomUsers]
	form.fields['name'].choices = formchoices
	request.session['choices'] = formchoices
	print "form choices created"

def random_user(used_names, names):
	names_set = set(names)
	used_names_set = set(used_names)
	not_used = list(names_set - used_names_set)
	
	rncorrect = not_used[random.randrange(0, len(not_used))]
	random_names = [rncorrect]
	for ind in range(0, 4):
		rn = names[random.randrange(0, len(names))]
		while rn in random_names:
			rn = names[random.randrange(0, len(names))]
		random_names.append(rn)
	random.shuffle(random_names)
	return random_names, rncorrect
