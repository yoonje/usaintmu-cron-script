import pymongo as mongo
import parser as ps

client = mongo.MongoClient('localhost', 27017) # 몽고DB 인스턴스 생성

db = client.usaintmu_db  # DB 생성

collection = db.lecture_collection  # Collection 생성

#document_id = documents.insert(ps.documents)  # _id를 자동으로 생성해서 DB에 insert <- db 스키마 정의 필요