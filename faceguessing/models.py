from django.db import models
import random

def random_user():
	names = ['aahv', 'atol', 'aker', 'aklu', 'akol', 'akos', 'alam', 'amat', 'apoi', 'aran', 'arau', 'avuo', 'cnis', 
	'eens', 'ejok', 'ekan', 'ekri', 'etan', 'evir', 'fbie', 'hdah', 'hhak', 'hhal', 'hhau', 'hhol', 'hkau', 'hnev', 
	'hsik', 'iiso', 'ileh', 'iram', 'jran', 'jero', 'jhud', 'jkai', 'jkak', 'jkan', 'jkar', 'jlep', 'jlid', 'jmer',
	'jpes', 'jris', 'jros', 'jsaa', 'jsuk', 'jvii', 'kink', 'kkol', 'ktuu', 'kzag', 'laht', 'lekl', 'lelo', 'lhag', 
	'lkol', 'llar', 'llem', 'lrom', 'ltan', 'maij', 'marv', 'mber', 'mbru', 'mcal', 'mhaa', 'mham', 'mhei', 'mleh', 
	'mjyl', 'mkap', 'mkos', 'mmal', 'mmat', 'mmul', 'mpii', 'mpor', 'msam', 'mtau', 'mvih', 'mvii', 'ndee', 'oaho', 
	'ohaa', 'ojar', 'okaj', 'omah', 'osal', 'ovan', 'phou', 'pjah', 'pjal', 'pkro', 'ppaa', 'ppul', 'pten', 'pves', 
	'rjar', 'rval', 'rsar', 'sber', 'sham', 'shyo', 'snum', 'spal', 'spiq', 'srot', 'ssaa', 'stau', 'tahv', 'tkor', 
	'thyv', 'tkaj', 'tkor', 'tmoi', 'tpaa', 'tpol', 'tsil', 'tsul', 'tsuo', 'tsyr', 'ttuo', 'ttur', 'tyla', 'valh', 
	'vizr', 'vkes', 'vman', 'vsaa', 'vsin', 'vtoi', 'ykar']
	
	rncorrect = names[random.randrange(0, len(names))]
	random_names = [rncorrect]
	for ind in range(0, 4):
		rn = names[random.randrange(0, len(names))]
		while rn in random_names:
			rn = names[random.randrange(0, len(names))]
		random_names.append(rn)

	random.shuffle(random_names)
	return random_names, rncorrect