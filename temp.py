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

# def scrapPullData() :
# 	f = open('repos', 'r')
# 	print f
# 	strn = f.read()
# 	lst = strn.split('\n')
# 	print lst[0]
# 	i = 0
# 	while i < (len(lst) - 1) :
# 	# while i < 1 :
# 		name = lst[i].split("/")

# 		try :
# 			base = "https://api.github.com/repos/" + lst[i] 

# 			base = base + "/pulls/888"

# 			print base

# 			r = requests.get(base)
# 			r.encoding = 'utf-8'		
# 			content = json.loads(r.text)

# 			fc = open(tempp.txt, 'w');
# 			fc.write(str(content))
# 			fc.close()

# 			print(lst[i] + "\t:\***********************************************completed")

		
# 		except : 
# 			print(lst[i]+"\t:\trequest error")

# 		sys.exit(0)
# 		i = i + 2

def scrapPullData():

	f = open('repos', 'r')
	strn = f.read()
	lst = strn.split('\n')
	print lst[0]
	i = 2
	while i < (len(lst) - 1) :
		name = lst[i].split("/")
		try :
			
			base = "https://api.github.com/repos/"+lst[i]+"/pulls"+"?access_token=215b77c3821dba3737b06c732d8db1db60f9afd4"
			print base

			r = requests.get(base)
			r.encoding = 'utf-8'		
			content = json.loads(r.text)
			#print "ddvvvv\n"
			
			
			for t in content:
				last = (t["url"].split('/'))[-1]
				break
				#time.sleep(10)
				#print t["url"]+"\n"
			last = int(last)
			
			pullsList=[]
			j=0
			while j<50:
				try:
					base = "https://api.github.com/repos/"+lst[i]+"/pulls/"+str(last)+"?access_token=215b77c3821dba3737b06c732d8db1db60f9afd4"
					print base
					r1 = requests.get(base)
				
					r1.encoding = 'utf-8'
						
					content = json.loads(r1.text)
					#print content

					if 'id' in content:
						pullsList.append(content)
						#print content
					last=int(last)-1
					j=j+1
				except:
					print "network lost"
					

			#print pullsList
			fc = open('data/'+name[1]+'/pulls.txt', 'w')

			#print "tererereererere"
			fc.write(str(pullsList))
			#print "dfkskvmksmvmskm"
			fc.close()
			# fc = open('data/'+name[1]+'/data.str', 'w');
			# fc.write(str(content))
			# fc.close()

			#sys.exit(0)
			i=i+2
		except : 
			print("request error")

		



scrapPullData()