import json, pandas
class Kimin_Core:
	def __init__(kimin, folder='db'):
		kimin.folder = folder
	
	def GetData(kimin, path='hasil.min'):
		hasil = []
		with open(f"{kimin.folder}/{path}") as dataku:
			data = dataku.read().splitlines()
		for i in data:
			hasil.append(json.loads(i))
		return hasil
	
	def Download_File(kimin):
		data = kimin.GetData()
		hasil = {}
		hasil['author'] = []
		hasil['content'] = []
		hasil['datepost'] = []
		hasil['reply'] = []
		hasil['retweet'] = []
		hasil['like'] = []
		hasil['penayangan'] = []
		for i in data:
			hasil['author'].append(i['author'])
			hasil['content'].append(i['content'])
			hasil['datepost'].append(i['datepost'])
			hasil['reply'].append(i['reply'])
			hasil['retweet'].append(i['retweet'])
			hasil['like'].append(i['like'])
			hasil['penayangan'].append(i['penayangan'])
		
		data = pandas.DataFrame(hasil)
		data.to_csv('Twitter.csv')
		