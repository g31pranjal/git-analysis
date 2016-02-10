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
import operator
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import numpy as np
import json


g = Github('b11cd88e5a7c991cd02645dbf2ed7d0d9c21ec0c')


# Scrapping the Github for README file and description !
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


#Scrapping repository statistics 
def scrapRepoData() :
	f = open('repos', 'r')
	strn = f.read()
	lst = strn.split('\n')

	i = 0
	while i < (len(lst) - 1) :
	# while i < 1 :
		name = lst[i].split("/")

		try :
			base = "https://api.github.com/repos/" + lst[i] 

			base = base + "?access_token=b11cd88e5a7c991cd02645dbf2ed7d0d9c21ec0c"

			print base

			r = requests.get(base)
			r.encoding = 'utf-8'		
			content = json.loads(r.text)

			fc = open('data/'+name[1]+'/data.str', 'w');
			fc.write(str(content))
			fc.close()

			print(lst[i] + "\t:\***********************************************completed")


		except : 
			print(lst[i]+"\t:\trequest error")


		i = i + 2


# Removing punctuations, stopwords and stemming. (refining the word list !)
def stopWordRemoval() :


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

		wordnet_lem= WordNetLemmatizer()


		ftf = open('filteredData/'+name[1]+'/title.lst','w')
		for w in filteredWordsTitle:
			#print w
			ftf.write(wordnet_lem.lemmatize(w)+'\n')

		fdf = open('filteredData/'+name[1]+'/description.lst','w')
		for w in filteredWordsDesc:
			#print w
			fdf.write(wordnet_lem.lemmatize(w)+'\n')

		fcf = open('filteredData/'+name[1]+'/content.lst','w')
		for w in filteredWordsData:
			print w+'\n'
			fcf.write(wordnet_lem.lemmatize(w)+'\n')
		
		i=i+2


# Calculating tf value of the keywords in a particular repository 
def keyword_tf() :

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
			if w in keyword_dict[name[1]] :
				keyword_dict[name[1]][w][0] += 1
			else :
				keyword_dict[name[1]][w] =  [1,0,0];

		for w in ld : 
			if w in keyword_dict[name[1]] :
				keyword_dict[name[1]][w][1] += 1
			else :
				keyword_dict[name[1]][w] =  [0,1,0];

		for w in lc : 
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
			keyword_dict[name[1]][w][0] = round(decimal.Decimal(float(keyword_dict[name[1]][w][0]*10000) / maxi),5)
			keyword_dict[name[1]][w][1] = round(decimal.Decimal(float(keyword_dict[name[1]][w][1]*100) / maxi),5)
			keyword_dict[name[1]][w][2] = round(decimal.Decimal(float(keyword_dict[name[1]][w][2]*1) / maxi),5)
		

		i=i+2

	f = open('keywords', 'w')

	f.write(str(keyword_dict))
	f.close()


# Calculating df value of all entities in keywords sets in all repositories 
def keyword_set_df() :
	keyword_set = set()

	f = open('repos', 'r')
	strn = f.read()
	lst = strn.split('\n')

	i = 0
	while i < (len(lst) - 1) :
	
		name = lst[i].split("/")

		ft = open('filteredData/'+name[1]+'/title.lst')
		lt = ft.read().split('\n')

		fd = open('filteredData/'+name[1]+'/description.lst')
		ld = fd.read().split('\n')

		fc = open('filteredData/'+name[1]+'/content.lst')
		lc = fc.read().split('\n')
		
		for w in lt : 
			keyword_set.add(w);

		for w in ld : 
			keyword_set.add(w);

		for w in lc : 
			keyword_set.add(w);

		i=i+2


	df = {}

	j = 0
	for keyword in keyword_set :
		i = 0
		j = j + 1

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


# calculate the weights of each keyword in the repository
def keyword_weight() :

	f1 = open('df', 'r')
	df = eval(f1.read())

	f2 = open('keywords', 'r')
	keyword_dict = eval(f2.read())

	keyword_1row = {}

	for repo in keyword_dict :
		keyword_1row[repo] = {}
		for word in keyword_dict[repo] :
			keyword_1row[repo][word] = 0
			idf_value = df[word][1]
			keyword_dict[repo][word][0] = round(decimal.Decimal(keyword_dict[repo][word][0]*idf_value),5)
			keyword_dict[repo][word][1] = round(decimal.Decimal(keyword_dict[repo][word][1]*idf_value),5)
			keyword_dict[repo][word][2] = round(decimal.Decimal(keyword_dict[repo][word][2]*idf_value),5)
			
	 		keyword_1row[repo][word] = keyword_dict[repo][word][0] + keyword_dict[repo][word][1] + keyword_dict[repo][word][2]

	f = open('repo-3row-vector.vct', 'w')

	f.write(str(keyword_dict))
	f.close()
	
	f = open('repo-1row-vector.vct', 'w')

	f.write(str(keyword_1row))
	f.close()


# 2-mean clusterring on the results to get a relevent set of results
def two_mean_od_cluster(lst) :

	assign_lst = [0]*len(lst)

	upperbnd = lst[0][1]
	lowerbnd = lst[len(lst) - 1][1]

	c1 = ((upperbnd - lowerbnd)*0.25) + lowerbnd
	c2 = ((upperbnd - lowerbnd)*0.75) + lowerbnd

	q1 = 0
	q2 = 0

	for i in range(0,10) : 
		j=0
		c1_num = 0
		c1_frq = 0
		c2_num = 0
		c2_frq = 0
		q2 = 0
		for repo in lst : 
			d1 = abs(c1 - repo[1])
			d2 = abs(c2 - repo[1])
			if d2 >= d1 : 
				assign_lst[j] = 1
				c1_num += repo[1]
				c1_frq += 1
			else : 
				q2 += 1
				assign_lst[j] = 2
				c2_num += repo[1]
				c2_frq += 1

			j = j + 1

		# print assign_lst

		try :
			c1 = c1_num / c1_frq
		except : 
			return 0

		try :
			c2 = c2_num / c2_frq
		except : 
			return len(lst)

		if(q1==q2) : 
			break;
		else : 
			q1 = q2

	trimmed = lst[:q2]


	return q2


# takes in the user query, forms a query vector and implements cosine similarity 
def query() :
	
	q = raw_input("enter the query ? \n")

	tokenizer = RegexpTokenizer(r'\w+')
	q = tokenizer.tokenize(q)
	wordnet_lem= WordNetLemmatizer()
	q = [wordnet_lem.lemmatize(w) for w in q if not w in stopwords.words('english')]

	mod1 = sqrt(len(q))

	f = open('repo-1row-vector.vct', 'r')
	keyword_data = eval(f.read())

	results = []

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
			tup = (repo, round((float(frequency)/len(q))*float(num)/(mod1*mod2),5))

			results.append(tup)

	results = sorted(results, key=lambda tup: tup[1], reverse = True)

	print "\n\nRanking of results based on search :: \n"

	for i in range(0,len(results)) : 
		print str(results[i])

	search_relevence_graph1(results)

	if (len(results) > 0) :
		qualified = two_mean_od_cluster(results)
	else : 
		qualified = 0

	# trimmed the list of results after 2-mean clusterring
	trimmed_search_results = results[:(qualified)]

	print "\n\ntrimmed results  based on search :: \n"

	for i in range(0,len(trimmed_search_results)) : 
	 	print trimmed_search_results[i]



	popularity_dict = get_popularity_index(trimmed_search_results)

	for i in range(0,len(trimmed_search_results)) : 
		pr = popularity_dict[trimmed_search_results[i][0]]
		rel_score = pr['score']

		effective_score = round(17/((10/trimmed_search_results[i][1]) + (7/rel_score)), 5)

		trimmed_search_results[i] += (rel_score, effective_score) 


	trimmed_search_results = sorted(trimmed_search_results, key=lambda tup: tup[3], reverse = True)


	print "\n\nRanking of trimmed results with popularity index based on search :: \n"

	for i in range(0,len(trimmed_search_results)) : 
	 	print trimmed_search_results[i]

	search_relevence_graph(trimmed_search_results)


	# for i in range(0,len(trimmed_search_results)) : 	
	# 	print str(trimmed_search_results[i])

	# search_relevence_graph(trimmed_search_results)



def get_popularity_index(results) :

	multiplier_s = 0.5
	multiplier_f = 0.3
	multiplier_w = 0.2
	
	popularity_data = {}

	i = 0
	max_stars = 0
	max_forks = 0

	for i in range(0,len(results)) :
		# print results[i][0]
		f = open("data/"+results[i][0]+"/data.str", 'r')
		obj = eval(f.read())
		repo = {}

		repo['created_at'] = obj['created_at']
		repo['stargazers_count'] = obj['stargazers_count']
		repo['forks_count'] = obj['forks_count']
		# repo['subscribers_count'] = obj['subscribers_count']
		repo['has_wiki'] = obj['has_wiki']

		if max_stars < obj['stargazers_count'] : 
			max_stars = obj['stargazers_count']

		if max_forks < obj['forks_count'] : 
			max_forks = obj['forks_count']

		popularity_data[results[i][0]] = repo


	for i in range(0,len(results)) :
		
		popularity_data[results[i][0]]['stargazers_count'] = round(popularity_data[results[i][0]]['stargazers_count']/float(max_stars),5)
		popularity_data[results[i][0]]['forks_count'] = round(popularity_data[results[i][0]]['forks_count']/float(max_forks),5)
		# repo['subscribers_count'] = obj['subscribers_count']
		
		if popularity_data[results[i][0]]['has_wiki'] == True : 
			popularity_data[results[i][0]]['has_wiki'] = 1
		else :
			popularity_data[results[i][0]]['has_wiki'] = 0


		popularity_data[results[i][0]]['score'] = round(multiplier_s*popularity_data[results[i][0]]['stargazers_count'] + multiplier_f*popularity_data[results[i][0]]['forks_count'] + multiplier_w*popularity_data[results[i][0]]['has_wiki'], 5)

	return popularity_data



def search_relevence_graph(results) :

	x = []
	y = []
	y1 = []
	y2 = []
	x_label = []

	for i in range(0, len(results)) :
		x.append(i+1)
		y.append(results[i][3])
		y1.append(results[i][1])
		y2.append(results[i][2])
		x_label.append(results[i][0])

	# print x
	# print y
	# print x_label

	plt.plot(x, y, 'ro')
	plt.plot(x, y1, 'bo')
	plt.plot(x, y2, 'go')
	plt.xticks(x, x_label, rotation='vertical')
	plt.margins(0.2)
	plt.subplots_adjust(bottom=0.15)
	plt.show()



def search_relevence_graph1(results) :

	x = []
	y1 = []
	x_label = []

	for i in range(0, len(results)) :
		x.append(i+1)
		y1.append(results[i][1])
		x_label.append(results[i][0])

	# print x
	# print y
	# print x_label

	plt.plot(x, y1, 'bo')
	plt.xticks(x, x_label, rotation='vertical')
	plt.margins(0.2)
	plt.subplots_adjust(bottom=0.15)
	plt.show()




# def graphs() :
# 	x = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5])

# 	print(np.amin(x))

# graphs()


# query("responsive css frameworks")

query()



