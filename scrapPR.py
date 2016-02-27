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
#import matplotlib.pyplot as plt
import numpy as np
import json
import sys
import time 
import datetime


def scrapPullData():

	f = open('repos', 'r')
	strn = f.read()
	lst = strn.split('\n')
	print lst[0]
	i = 0
	while i < (len(lst) - 1) :
		name = lst[i].split("/")
		print name
		#try :
			
		base = "https://api.github.com/repos/"+lst[i]+"/pulls"+"?state=all&access_token=8827a3eca16efdfcbf58035c87c9a8909b03f3d1"
		print base

		r = requests.get(base)
		r.encoding = 'utf-8'		
		content = json.loads(r.text)
		#print "ddvvvv\n"

		
		for t in content :
			last_numb = t['number'] + 2
			last_time = datetime.datetime.strptime(t['created_at'], '%Y-%m-%dT%H:%M:%SZ')
			break

		last_numb = int(last_numb)
		
		pullsList=[]
	 	j=0
	 	td = datetime.datetime.now() - datetime.datetime.now()
	 	while td.days < 60:
	 		try:
				base = "https://api.github.com/repos/"+lst[i]+"/pulls/"+str(last_numb)+"?access_token=8827a3eca16efdfcbf58035c87c9a8909b03f3d1"
				print base
				r1 = requests.get(base)
				r1.encoding = 'utf-8'
				content = json.loads(r1.text)
					
				#p_time = datetime.datetime.strptime(content['created_at'], '%Y-%m-%dT%H:%M:%SZ')

				print content.keys()

				if u'message' in content.keys() :
					print "not a pull"
				else :
					print "is a pull request !"
					obj = {}
					obj['created_at'] = datetime.datetime.strptime(content['created_at'], '%Y-%m-%dT%H:%M:%SZ')
					obj['number'] = content['number']
					obj['state'] = content['state']
					obj['merged_at'] = content['merged_at']

					td = last_time - obj['created_at']

					print td.days 

				 	pullsList.append(obj)
				
				last_numb = int(last_numb) - 1
				j=j+1

			except:
				print "network lost"

				

		fc = open('data/'+name[1]+'/pulls.data', 'w')
		fc.write(str(pullsList))
		fc.close()

		i = i+2

scrapPullData()