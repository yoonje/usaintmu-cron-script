import pymongo as mongo
import parser as ps

client = mongo.MongoClient('localhost', 27017)  # 몽고DB 인스턴스 생성

db = client.usaintmu_db  # DB 생성

collection = db.lecture_collection  # Collection 생성

if __name__ == "__main__":
    # 전공은 주전공 이수구분에 따라서 중복이 생기므로 처리 해줘야함(이수구분(주전공) plus and not insert)
    for major_document in ps.major_documents:
        if collection.find({"과목번호": major_document["과목번호"]}) == True:
            collection.update({"과목번호": major_document["과목번호"]}, {"$push": {"과목번호": major_document["과목번호"]}})
        else:
            collection.insert(major_document)

    for essential_document in ps.essential_documents:
        collection.insert(essential_document)

    # 교선은 교과영역에 따라서 중복이 생기므로 처리해줘야함(not insert)
    for selective_document in ps.selectives_documents:
        if collection.find({"과목번호": selective_document["과목번호"]}) == True:
            pass
        else:
            collection.insert(selective_document)
