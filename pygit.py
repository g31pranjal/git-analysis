import pymongo
import github

from github import Github
from pymongo import MongoClient

mongo = MongoClient()


def hello() :
	winterfixs = mongo['winterfixs']
	winterfixs.randomshit.insert_one({"name" : "pranjal gupta", "age" : 21})

def gitconnect() :
	g = Github("1d887e63cc6eba9fd5e57ea918801f7c832d1cb5")
	repo = g.get_repo("angular/angular");
	print repo.forks_count


gitconnect()


hello()

