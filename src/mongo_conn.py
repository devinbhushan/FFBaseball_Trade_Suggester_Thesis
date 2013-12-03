from pymongo import MongoClient

def get_client():
	client = MongoClient('mongodb://thesis:baseball@dharma.mongohq.com:10055/fbaseball_thesis')
	return client