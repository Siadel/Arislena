# -*-coding : utf-
from openpyxl import *

suprasegmental = False

dodgable = False

ipable = True
hanjable = True
englishable = False
koreanable = False

filename = 'ipa.xlsx'

book = load_workbook(filename)
ph = book['ph']
syl = book['syl']
pho = book['pho']

Ph = dict()
for r in ph.rows:
	
	key = r[0].value
	lis = []
	for v in r:
		if v.column == 1:
			continue
		else:
			lis.append(v.value)
	
	Ph.setdefault(key, lis)
	
for rows in [syl.rows, pho.rows]:
	for r in rows:
		for cr in r:
			cr.value = None



def level(string):
	for st in string:
		tst = Ph[st][3]
		if type(tst) == str:
			return tst

test = 'xei'


dresult = {
		'ipa_convert' : None,
		'CV' : None,
		'meaning_hanja' : None,
		'meaning_english' : None,
		'meaning_korean' : None
		}
		
def exe(sentence):
	
	lower = sentence.lower()
	lower = lower.strip()
	
	words = lower.split(' ')
	
	isyl = 1
	iphr = 1
	
	lconv = []
	lCV = []
	lmh = []
	lme = []
	lmk = []
	for word in words: 
		syl[f'A{isyl}'].value = word
		iphc = 3
		
		li = []
		parsed = []
		for s in word: # eumso parsing 1
			idx = word.index(s)
			next = word[idx+1] if idx < len(word)-1 else False
			
			C = Ph[s][0]
			J = Ph[s][5]
			H = Ph[s][6]
			
			if next is False:
				li.append(len(word))
				break
				
			if C != Ph[next][0]:
				li.append(idx+1)
			elif C == 'V':
				li.append(idx+1)
			else:
				if C == 'C':
					if not ((J and next=='j') or (H and next=='h')):
						li.append(idx+1)
	
		
		for l in li: # eumso parsing 2
			
			idx = li.index(l)
			pre = li[idx-1] if idx >= 1 else False
			next = li[idx+1] if idx < len(li)-1 else False
				
			start = 0 if pre == False else pre
			end = l if next != False else len(word)
			
			parse = word[start:end]
			parsed.append(parse)
			
		lipa = []
		lcv = []
		lhanja = []
		leng = []
		lkor = []
		for p in parsed: # making eumso data
			
			idx = parsed.index(p)
			pre = parsed[idx-1] if idx >= 1 else False
			next = parsed[idx+1] if idx < len(parsed)-1 else False
			
			syl.cell(row=isyl, column=iphc).value = p
			
			search = Ph[p]
			
			C = search[0]
			ipa = search[1]
			allo = search[2]
			dodge = search[3]
			
			if C == 'C': # allophone
				if pre == 'x':
					
					if allo is not None:
						if dodgable:
							if dodge:
								ipa = pre+p
							if not dodge:
								ipa = allo
						else:
							ipa = allo
					else:
						pass
			
			elif C == 'V':
				if (Ph[pre][0] == 'C' and Ph[pre[0]][5]) and allo is not None:
					ipa = allo
				if next is not False:
					if Ph[next][0] == 'V':
						ipa = ipa[0] + '̯'
						
			if p == 'x' and (Ph[next][0] == 'C' and Ph[next][2] is not None):
				ipa = ''
			
			meaning_hanja = Ph[search[4]][7] if C == 'V' else search[7]
			meaning_english = Ph[search[4]][8] if C == 'V' else search[8]
			meaning_korean = Ph[search[4]][9] if C == 'V' else search[9]
			
			pho[f'A{iphr}'].value = p
			
			pho[f'B{iphr}'].value = C
			lcv.append(C)
			pho[f'C{iphr}'].value = ipa if ipable else None
			lipa.append(pho[f'C{iphr}'].value)
			pho[f'D{iphr}'].value = meaning_hanja if hanjable else None
			lhanja.append(pho[f'D{iphr}'].value)
			pho[f'E{iphr}'].value = meaning_english if englishable else None
			leng.append(pho[f'E{iphr}'].value)
			pho[f'F{iphr}'].value = meaning_korean if koreanable else None
			lkor.append(pho[f'F{iphr}'].value)
			
			iphc += 1
			iphr += 1
		
		lCV.append(''.join(lcv))
		
		if None in lipa:
			pass
		else:
			lconv.append(''.join(lipa))
		if None in lhanja:
			pass
		else:
			lmh.append(''.join(lhanja))
		if None in leng:
			pass
		else:
			lme.append(''.join(leng))
		if None in lkor:
			pass
		else:
			lmk.append(''.join(lkor))
		
		isyl += 1
	
	ipa = []
	for rsyl in syl.rows:
		
		lii = []
		
		for csyl in rsyl[2:9]:
			if csyl.value is None:
				continue
			
			lii.append(Ph[csyl.value][0])
		
		syl[f'J{rsyl[0].row}'].value = ''.join(lii)
	
	dresult.update({'CV' : ' '.join(lCV)})
	if len(lconv) == 0:
		pass
	else:
		dresult.update({'ipa_convert' : ' '.join(lconv)})
	if len(lmh) == 0:
		pass
	else:
		dresult.update({'meaning_hanja' : ' '.join(lmh)})
	if len(lme) == 0:
		pass
	else:
		dresult.update({'meaning_english' : ' '.join(lme)})
	if len(lmk) == 0:
		pass
	else:
		dresult.update({'meaning_korean' : ' '.join(lmk)})
	
	print(dresult)

	book.save(filename)
	book.close()


print(exe(test))