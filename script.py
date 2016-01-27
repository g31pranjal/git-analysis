import requests 
from github import Github
import os

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



	# r = requests.get(base)

	# f = open('file', 'w')
	# f.write(r.content)
	# f.close()

	# print(r.content)
	

	# print(base)

	
scrap()
