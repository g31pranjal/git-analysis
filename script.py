import requests 
from github import Github
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from stemming.paicehusk import stem

g = Github('11f05f96a85f334542c789e5b5118d9dbf6c60c3')

def scrap() : 
	f = open('repos', 'r')
	strn = f.read()
	lst = strn.split('\n')

	i = 0
	while i < (len(lst) - 1) :
		name = lst[i].split("/")


		dummyFile = 'data/' + name[1] + '/dummy.txt';
		dr = os.path.dirname(dummyFile)

		if not os.path.exists(dr) :
			os.makedirs(dr)



		try :
			repo = g.get_repo(lst[i])

			title = repo.name
			desc = repo.description
			print(title)
			print(desc)

			ft = open('data/'+name[1]+'/title.txt', 'w');
			fd = open('data/'+name[1]+'/description.txt', 'w');

			ft.write(title)
			fd.write(desc)

			ft.close()
			fd.close()

		except :
			print("pygithub error")



		try :
			base = "https://raw.githubusercontent.com/" + lst[i] + "/master/" + lst[i+1]

			r = requests.get(base)
			r.encoding = 'utf-8'		
			content = r.text		

			fc = open('data/'+name[1]+'/content.txt', 'w');

			fc.write(content.encode('utf-8'))

			fc.close()

		except : 
			print("request error")


		i = i + 2


def stopWordRemoval() :
	
	# stemmer= PorterStemmer()

	# stemmedArr=[]

	# for word in filteredWords:
	# 	stemmedWord= stemmer.stem(word)
	# 	stemmedArr.append(stemmedWord)

	# print stemmedArr

	f = open('repos', 'r')
	strn = f.read()
	lst = strn.split('\n')

	i = 0
	while i < (len(lst) - 1) :
	
		name = lst[i].split("/")

		dummyFile = 'filteredData/' + name[1] + '/dummy.txt';
		dr = os.path.dirname(dummyFile)

		if not os.path.exists(dr) :
			os.makedirs(dr)

		ft = open('data/'+name[1]+'/title.txt')
		st = ft.read().lower()

		fd = open('data/'+name[1]+'/description.txt')
		sd = fd.read().lower()

		fc = open('data/'+name[1]+'/content.txt')
		sc = fc.read().lower()
		

		tokenizer = RegexpTokenizer(r'\w+')

		wordArrTitle = tokenizer.tokenize(st)
		wordArrDesc = tokenizer.tokenize(sd)
		wordArrData = tokenizer.tokenize(sc)

		filteredWordsTitle = [w for w in wordArrTitle if not w in stopwords.words('english')]
		filteredWordsDesc = [w for w in wordArrDesc if not w in stopwords.words('english')]
		filteredWordsData = [w for w in wordArrData if not w in stopwords.words('english')]

		ftf = open('filteredData/'+name[1]+'/title.lst','w')
		for w in filteredWordsTitle:
			#print w
			ftf.write(w+'\n')

		fdf = open('filteredData/'+name[1]+'/description.lst','w')
		for w in filteredWordsDesc:
			#print w
			fdf.write(w+'\n')

		fcf = open('filteredData/'+name[1]+'/content.lst','w')
		for w in filteredWordsData:
			print w+'\n'
			fcf.write(w+'\n')
		
		i=i+2


def stemTest() :

	fc = open('data/django/content.txt')
	sc = fc.read().lower()

	print sc + "\n"

	tokenizer = RegexpTokenizer(r'\w+')
	wordArrData = tokenizer.tokenize(sc)

	filteredWordsData = [w for w in wordArrData if not w in stopwords.words('english')]

	stemmedData = []

	# stemmer = PorterStemmer();

	for word in filteredWordsData :
		stemmedData.append(stem(word))

	print stemmedData


def keywords() :
	keyword_set = set()

	keyword_dict = {}

	f = open('repos', 'r')
	strn = f.read()
	lst = strn.split('\n')

	i = 0
	while i < (len(lst) - 1) :
	
		name = lst[i].split("/")

		keyword_dict[name[1]] = {}

		ft = open('filteredData/'+name[1]+'/title.lst')
		lt = ft.read().split('\n')

		fd = open('filteredData/'+name[1]+'/description.lst')
		ld = fd.read().split('\n')

		fc = open('filteredData/'+name[1]+'/content.lst')
		lc = fc.read().split('\n')
		
		for w in lt : 
			keyword_set.add(w);
			if w in keyword_dict[name[1]] :
				keyword_dict[name[1]][w][0] += 1
			else :
				keyword_dict[name[1]][w] =  [1,0,0];

		for w in ld : 
			keyword_set.add(w);
			if w in keyword_dict[name[1]] :
				keyword_dict[name[1]][w][1] += 1
			else :
				keyword_dict[name[1]][w] =  [0,1,0];

		for w in lc : 
			keyword_set.add(w);
			if w in keyword_dict[name[1]] :
				keyword_dict[name[1]][w][2] += 1
			else :
				keyword_dict[name[1]][w] =  [0,0,1];

		i=i+2

	f = open('keywords', 'w')

	f.write(str(keyword_dict))
	f.close()


	df = {}

	j = 0
	for keyword in keyword_set :
		i = 0
		j = j + 1

		print("word "+str(j)+"\t"+keyword)

		df[keyword] = 0

		while i < (len(lst) - 1) :
		
			name = lst[i].split("/")

			i=i+2

			ft = open('filteredData/'+name[1]+'/title.lst')
			lt = ft.read().split('\n')

			fd = open('filteredData/'+name[1]+'/description.lst')
			ld = fd.read().split('\n')

			fc = open('filteredData/'+name[1]+'/content.lst')
			lc = fc.read().split('\n')


			if keyword in lt :
				df[keyword] = df[keyword] + 1
				continue
			

			if keyword in ld :
				df[keyword] = df[keyword] + 1
				continue
			

			if keyword in lc :
				df[keyword] = df[keyword] + 1
				continue
			



		print keyword +"  :  "+str(df[keyword])+ "\n"


	f = open('df', 'w')

	f.write(str(df))
	f.close()


	# print df






keywords()