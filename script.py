import requests 
from github import Github
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from stemming.paicehusk import stem
from math import *
import decimal


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

	keyword_max = {}

	f = open('repos', 'r')
	strn = f.read()
	lst = strn.split('\n')

	i = 0
	while i < (len(lst) - 1) :
	
		name = lst[i].split("/")

		keyword_dict[name[1]] = {}
		keyword_max[name[1]] = 0

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

		maxi = 0
		for w in keyword_dict[name[1]] : 
			if(keyword_dict[name[1]][w][0] + keyword_dict[name[1]][w][1] + keyword_dict[name[1]][w][2] > maxi) :
				maxi = keyword_dict[name[1]][w][0] + keyword_dict[name[1]][w][1] + keyword_dict[name[1]][w][2]
		
		keyword_max[name[1]] = maxi

		for w in keyword_dict[name[1]] : 
			keyword_dict[name[1]][w][0] = round(decimal.Decimal(float(keyword_dict[name[1]][w][0]*1000000) / maxi),5)
			keyword_dict[name[1]][w][1] = round(decimal.Decimal(float(keyword_dict[name[1]][w][1]*10000) / maxi),5)
			keyword_dict[name[1]][w][2] = round(decimal.Decimal(float(keyword_dict[name[1]][w][2]*100) / maxi),5)
		


		i=i+2



	f = open('keywords', 'w')

	f.write(str(keyword_dict))
	f.close()

	# print keyword_max


	df = {}

	j = 0
	for keyword in keyword_set :
		i = 0
		j = j + 1

		# print("word "+str(j)+"\t"+keyword)

		df[keyword] = [0,0]

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
				df[keyword][0] = df[keyword][0] + 1
				continue
			

			if keyword in ld :
				df[keyword][0] = df[keyword][0] + 1
				continue
			

			if keyword in lc :
				df[keyword][0] = df[keyword][0] + 1
				continue
			

		df[keyword][1] = log((float(44.0)/df[keyword][0]),2)

		df[keyword][1] = round(decimal.Decimal(df[keyword][1]),3)

		# print keyword +"  :  "+str(df[keyword][0])+"  :  "+str(df[keyword][1])+ "\n"


	f = open('df', 'w')

	f.write(str(df))
	f.close()


	# print df

	keyword_1row = {}

	for repo in keyword_dict :
		keyword_1row[repo] = {}
		for word in keyword_dict[repo] :
			keyword_1row[repo][word] = 0
			#print keyword_dict[repo][word]+"\n"
			idf_value = df[word][1]
			keyword_dict[repo][word][0] = round(decimal.Decimal(keyword_dict[repo][word][0]*idf_value),5)
			keyword_dict[repo][word][1] = round(decimal.Decimal(keyword_dict[repo][word][1]*idf_value),5)
			keyword_dict[repo][word][2] = round(decimal.Decimal(keyword_dict[repo][word][2]*idf_value),5)
			# print word+" : "+str(idf_value)+"\n"
			
			keyword_1row[repo][word] = keyword_dict[repo][word][0] + keyword_dict[repo][word][1] + keyword_dict[repo][word][2]

	f = open('repo-3row-vector-.vct', 'w')

	f.write(str(keyword_dict))
	f.close()
	
	f = open('repo-1row-vector-.vct', 'w')

	f.write(str(keyword_1row))
	f.close()


def query() :
	
	q = raw_input("enter the query ? \n")

	tokenizer = RegexpTokenizer(r'\w+')
	q = tokenizer.tokenize(q)
	q = [w for w in q if not w in stopwords.words('english')]

	mod1 = sqrt(len(q))

	f = open('repo-1row-vector-.vct', 'r')
	keyword_data = eval(f.read())

	results = {}

	# print keyword_data

	for repo in keyword_data : 
		num = 0
		mod2 = 0
		frequency = 0

		for word in keyword_data[repo] : 
			if word in q : 
				num = num + keyword_data[repo][word]
				mod2 = mod2 + pow(keyword_data[repo][word],2)
				frequency = frequency + 1


		mod2 = sqrt(float(mod2))

		if mod2==0 :
			pass
		else :
			print str(num) +" : "+str(mod2)+"\n"
			results[repo] = (float(frequency)/len(q))*float(num)/(mod1*mod2)





	for result in results :
		print result+"\t:\t"+str(results[result])+"\n"



