from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from fumapi.utils import query
from django import forms
import random

class NameForm(forms.Form):
	name = forms.ChoiceField(widget = forms.RadioSelect)

def index(request):
	print "start"
	if request.method == 'POST':
		print "Posted!"
		times = request.session['times']
		print times
		#if times < 5:
		times += 1
		print times
		request.session['times'] = times
			#print times
		print "Sessions:"
		print dict(request.session)
		random_users, correct_user = request.session['namesession']
		prev_correct_user = correct_user
		form = NameForm(request.POST, initial={'name': random_users})
		form.fields['name'].choices = [(user, query('user', user)['cn']) for user in random_users]
		if correct_user == request.POST['name']:
			print "GOOD ANSWER !!!"
			if form.is_valid():
				print "VALID FORM"
				form = NameForm()
				#name = form.cleaned_data['name']
				request.session.pop('namesession', None)

				used_names = request.session.setdefault('used_names', [])
				times = request.session['times']

				random_users, correct_user = random_user(used_names)
				used_names.append(correct_user)
				form.fields['name'].choices = [(user, query('user', user)['cn']) for user in random_users]
				request.session['namesession'] = random_users, correct_user
				request.session['used_names'] = used_names
				print used_names
				print correct_user
				#{'html': generated_form, 'rnCorrect': correct_user}
				{'rnCorrect': correct_user}
				return render_to_response('form.html', {'form': form, 'rncorrect': correct_user, 'time': times, 'prevrncorrect': prev_correct_user},
				context_instance=RequestContext(request))
				#return render_to_response('test.html', context_instance=RequestContext(request))
		else:
			print "WRONG ANSWER"
			print "I don't even know how you got here"
		#else:
		#	request.session.pop('used_names', None)
		#	request.session.pop('times')
		#	return HttpResponseRedirect('/thegame/')
	else:
		print "else"
		form = NameForm()
		used_names = []
		request.session['used_names'] = used_names
		times = 0
		request.session['times'] = times

	random_users, correct_user = random_user(used_names)
	used_names.append(correct_user)
	print "blabla"
	print times
	form.fields['name'].choices = [(user, query('user', user)['cn']) for user in random_users]
	print "blooaa"
	request.session['namesession'] = random_users, correct_user
	request.session['used_names'] = used_names
	print used_names
	return render_to_response('template.html', {'form': form, 'rncorrect': correct_user, 'time': times})

def random_user(used_names):
	names = ['ileh', 'tkaj', 'hnev', 'mtau', 'hdah', 'jpes', 'mcal', 'hkau', 'ekan', 'sham', 'pjal', 'mvih',
	'thyv', 'jran', 'ssaa', 'kzag', 'okaj', 'hhol', 'mhei', 'ekri', 'rjar', 'tmoi', 'lkol', 'ltan', 'tkai', 'vman', 'omah',
	'arau',	'msam', 'llem', 'mmul', 'tfor', 'jkal', 'evir', 'tpaa', 'osal', 'llar', 'mber', 'hhal', 'alam', 'vtoi', 'ttuo',
	'mvii',	'mjyl', 'mbru', 'tsuo', 'ttia', 'ttur', 'vsaa', 'jris', 'oaho', 'jlid', 'sber', 'jros', 'vizr', 'maij', 'lelo', 
	'ppul', 'cven', 'iiso', 'mpor', 'tyla', 'mmal', 'mkos', 'ojar', 'iram', 'jkan', 'jmer', 'valh', 'stau', 'kkol',
	'asal',	'akar', 'jkar', 'mpii', 'hhak', 'pjah', 'lrom', 'ovan', 'jvii', 'pten', 'marv', 'spal', 'apoi', 'akos', 'tkor',
	'jkai',	'phou', 'mile', 'aahv', 'kink', 'hsik', 'akol', 'jlep', 'etan', 'mkap', 'pkro', 'mmat', 'ohaa', 'srot', 'snum',
	'vsin',	'avuo', 'laht', 'jero', 'tmar', 'jsuk', 'aker', 'tsul', 'jara', 'ejok', 'jkak', 'jhud', 'ykar', 'shyo', 'amat',
	'vkes',	'lekl', 'pves', 'jsaa', 'mham', 'cnis', 'aklu', 'fbie', 'tsil', 'ktuu', 'teko', 'rsar', 'tahv', 'spiq', 'ppaa', 'dnai', 'rama']
	names_set = set(names)
	used_names_set = set(used_names)
	not_used = list(names_set - used_names_set)
	print "names are set"
	
	rncorrect = not_used[random.randrange(0, len(not_used))]
	random_names = [rncorrect]
	print "looping"
	for ind in range(0, 4):
		rn = names[random.randrange(0, len(names))]
		while rn in random_names:
			rn = names[random.randrange(0, len(names))]
		random_names.append(rn)
	print "done looping"
	random.shuffle(random_names)
	print "done shuffling"
	return random_names, rncorrect
