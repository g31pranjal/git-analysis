import requests 
from github import Github
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

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
	
	# stemmer= SnowballStemmer('english')

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


stopWordRemoval()

