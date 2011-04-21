from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from fumapi import read, read_list
from django import forms
from models import Player
import random

class NameForm(forms.Form):
	name = forms.ChoiceField(widget = forms.RadioSelect)

def index(request):
	player, create = Player.objects.get_or_create(playerid="jsaa")
	if create:
		player.currentCorrectUser = ''
		player.currentRandomUsers = []
		player.usednames = []
		player.stats = {}
	names = request.session.setdefault('names', getAllNames())
	if request.method == 'POST':
		#session = dict(request.session)
		#random_users, correct_user = request.session['namesession']
		#random_users = player.currentRandomUsers
		#correct_user = player.currentCorrectUser
		form = NameForm(request.POST, initial={'name': player.currentRandomUsers})
		if 'choices' not in request.session:
			form.fields['name'].choices = [(user, read('user', user)['cn']) for user in player.currentRandomUsers]
		else:
			formchoices = request.session['choices']
			form.fields['name'].choices = formchoices
		if correct_user == request.POST['name']:
			if form.is_valid():
				form = NameForm()
				#request.session.pop('namesession', None)
				#used_names = request.session.setdefault('used_names', [])
				#used_names = player.usednames
				player.currentRandomUsers, player.currentCorrectUser = random_user(used_names, names)
				#used_names.append(correct_user)
				player.usednames += [player.currentCorrectUser]
				user_dicts = [read('user', user) for user in player.currentRandomUsers]
				formchoices = [(user['uid'], user['cn']) for user in user_dicts]
				#formchoices = [(user, read('user', user)['cn']) for user in player.currentRandomUsers]
				form.fields['name'].choices = formchoices
				request.session['choices'] = formchoices
				#request.session['namesession'] = random_users, correct_user
				#request.session['used_names'] = used_names
				#{'rnCorrect': correct_user}
				return render_to_response('form.html', {'form': form, 'rncorrect': player.currentCorrectUser}, context_instance=RequestContext(request))
			else:
				print "form was not valid"
		else:
			print "form had invalid name, probably because it was posted twice"
	form = NameForm()
	#used_names = []
	#request.session['used_names'] = used_names
	request.session.pop('choices', None)
	player.currentRandomUsers, player.currentCorrectUser = random_user(player.usednames, names)
	player.usednames += [player.currentCorrectUser]
	form.fields['name'].choices = [(user, read('user', user)['cn']) for user in player.currentRandomUsers]
	#request.session['namesession'] = random_users, correct_user
	#request.session['used_names'] = used_names
	return render_to_response('template.html', {'form': form, 'rncorrect': player.currentCorrectUser}, context_instance=RequestContext(request, {}))

#def filternames():
#	names = [user['uid'] for user in read_list('user')]
#	filterednames = []
#	for name in names:
#		if len(name) < 5:
#			filterednames.append(name)
#	return filterednames

def getAllNames():
	names = read('group', 'Futurice')['uniqueMember']
	return names

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
