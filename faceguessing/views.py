from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from faceguessing.models import random_user
from fumapi.utils import query
from django import forms

class NameForm(forms.Form):
	name = forms.ChoiceField(widget = forms.RadioSelect)

def index(request):
	if request.method == 'POST':
		random_users, correct_user = request.session['namesession']
		form = NameForm(request.POST, initial={'name': random_users})
		form.fields['name'].choices = [(user, query('user', user)['cn']) for user in random_users]
		if correct_user == request.POST['name']:
			print "GOOD ANSWER !!!"
			if form.is_valid():
				print "VALID FORM"
				name = form.cleaned_data['name']
				request.session.pop('namesession', None)
				return HttpResponseRedirect('/thegame/')
		else:
			print "WRONG ANSWER"
	else:
		form = NameForm()
	random_users, correct_user = random_user()
	form.fields['name'].choices = [(user, query('user', user)['cn']) for user in random_users]
	request.session['namesession'] = random_users, correct_user
	return render_to_response('template.html', {'form': form, 'rncorrect': correct_user})