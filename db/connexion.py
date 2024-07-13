import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

crawlerV2 = client.crawlerv3

queue = crawlerV2.queue
already_rq = crawlerV2.validated