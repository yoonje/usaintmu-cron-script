import pymongo as mongo

client = mongo.MongoClient('localhost', 27017)
# client = mongo.MongoClient('mongodb://localhost:27017/')
# client = mongo.MongoClient()

db = client["test_db"]  # test_db라는 이름으로 db 생성
# db = client.test_db
collection = db["test_collection"]  # test_collection라는 이름으로 collection 생성
# collection = db.test_collction

document = {
               "계획": " ",
               "이수구분(주전공)": "전선-기독교",
               "이수구분(다전공)": ["복선-기독교","부선-기독교"],
               "공학인증": " ",
               "교과영역": "7+1교과목\n인턴쉽(장기과정)\n인턴쉽",
               "과목번호": "5010611601",
               "과목명": "국내장기현장실습(3)",
               "분반": " ",
               "교수명": " ",
               "개설학과": "경력개발팀",
               "시간/학점(설계)": "3.00 /3",
               "수강인원": "5",
               "여석": "0",
               "강의시간(강의실)": " ",
               "수강대상": "전체",
               "year": "2017",
               "semester": "2"
               },

documents = db["documents"]
# posts = db.posts

document_id = documents.insert(document)  # _id를 자동으로 생성해서 insert

collection.remove("posts")
print(db.collection_names())
print(document_id)
print(documents.find_one())
