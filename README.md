
# Soongsil University Timetable Appliction Server
숭실대 수강신청 정보를 전송을 위해 pysaint와 pymongo를 사용하여 cron script을 작성합니다. 수강신청 정보를 설정된 주기에 따라 MongoDB에 저장합니다. 이후 웹 애플리케이션을 통해 변경된 최신 수강 신청 정보를 사용자에게 전달할 수 있습니다.

### Version
- Python: 3.6.8
- MongoDB: 3.4.0
- pymongo: 3.8.0
- pysaint: 1.5.2
- mongoengine 0.18.2

### Installation
```sh
$ sudo pip install -r requirements.txt
```


### Run 
```sh
$ ./manage.py runserver or python3 manage.py runserver
```

### Document Shape
JSON 파일에 년도와 학기 그리고 시간에 해당하는 키와 값(리스트)을 추가했고 이수구분(주전공) 키들의 값을 리스트로 변경했습니다.

ex) 

```js
document = {
     'semester': '2 학기',
     'time': ['수 18:00-18:50', '수 19:00-19:50', '목 18:00-18:50', '목 19:00-19:50'],
     'year': '2019',
     '강의시간(강의실)': '수 18:00-18:50 (정보과학관 21305 이철희강의실-김익수)\n'
                  '수 19:00-19:50 (정보과학관 21305 이철희강의실-김익수)\n'
                  '목 18:00-18:50 (정보과학관 21305 이철희강의실-김익수)\n'
                  '목 19:00-19:50 (정보과학관 21305 이철희강의실-김익수)',
     '개설학과': '융합특성화자유전공학부',
     '계획': '\xa0',
     '공학인증': '\xa0',
     '과목명': '프로그래밍및실습',
     '과목번호': '2150036403',
     '교과영역': '\xa0',
     '교수명': '김익수\n김익수\n김익수\n김익수',
     '분반': '\xa0',
     '수강대상': '1학년 자유전공학부',
     '수강인원': '0',
     '시간/학점(설계)': '4.00 /3.0',
     '여석': '30',
     '이수구분(다전공)': '\xa0',
     '이수구분(주전공)': ['전기-융합특성화']
}
```

### MongoDB Shell

##### - run & stop
```sh
$ sudo serverice mongod start
```
몽고DB를 실행한다.
```sh
$ mongo
```
몽고DB shell 실행한다.
```sh
$ sudo serverice mongod stop
```
몽고DB를 종료한다.

##### - create
```sh
> use <database_name> 
```
<database_name>에 맞는 database를 생성한다.
이미 존재할 경우 해당 db를 사용한다.
```sh
> db
```
현재 사용 중인 database를 확인한다.
```sh
> show dbs
```
데이터 베이스 리스트를 확인한다.
```sh
> db.<collection 이름>.insert(<추가할 document>)
```
1개 이상의 document를 추가해야 database가 실제로 생성된다. 또한 여러 개의 document를 한번에 insert 할 수 있다. document의 _id는 임의로 생성 된다.
##### - read
```sh
> show collections
or
> db.getCollectionNames()
```
collection list를 확인한다.
```sh
> db.<collection 이름>.find(<선택 기준(query)>,<선택 결과에 포함될 필드>)
or
> db.<collection 이름>.find(<선택 기준(query)>,<선택 결과에 포함될 필드>).pretty()
```
find()함수에 아무 인자도 주지 않을 경우 collection 내의 모든 document를 선택한다. 두번째 인자를 사용할 경우 선택 기준 인자에 {}를 넣어 아무 인자도 넣지 않음을 표시한다. 이는 다른 API에서도 동일하다. pretty()를 사용하면 return data를 format에 맞게 출력한다. 쿼리 연산자를 이용하여 쿼리 옵션을 쉽게 표현할 수 있다.<br><br>
비교 연산자\
<img src="image/compare.png" width="600" height="330">

논리 연산자\
<img src="image/logic.png" width="600" height="200">

##### - update
```sh
> db.<collection 이름>.update(
    <선택 기준(query)>,
    <update할 내용>,
    {
      upsert: <boolean>,
      multi: <boolean>,
      writeConcern: <document>
    }
)
```
선택 기준에 따라 update할 대상을 선택한다. upsert를 true로 하면 선택 기준에 맞는 Document가 없을 경우 insert한다. multi를 true로 하면 선택 기준에 맞는 document들을 모두 update한다. false일 경우 하나의 document만 update한다. wrtieConcern은 영속화를 위한 설정인데 자주 사용하지 않는다. 해당 옵션들은 default가 false이다.

MongoDB Update field operator\
<img src="image/field.png" width="600" height="350">
##### - delete 
```sh
> db.collection.remove(
  <선택 기준(query)>,
  {
    justOne: <boolean>,
    writeConcern: <document>
  }
)
```
선택 기준에 따라 delete할 대상을 선택한다. justOne을 true로 하면 기준에 맞는 Document를 1개 삭제한다. wrtieConcern은 영속화를 위한 설정인데 자주 사용하지 않는다. 해당 옵션들은 default가 false이다.
```sh
> db.<collection 이름>.drop()
```
해당 collection을 삭제한다.
```sh
> db.dropDatabase()
```
Database를 삭제한다.


### Pymongo API

##### - create
```python
# 몽고DB 인스턴스 얻기
<몽고DB 인스턴스 이름 사용자 정의> = pymongo.MongoClient(<몽고DB 설치 IP>,<포트>)
```
MongoClient를 돌고 있는 mongoDB 인스턴스를 생성한다.
```python
# DB 얻기
<데이터베이스 참조 변수> = <정의한 몽고DB 인스턴스>.<데이터베이스 이름 사용자 정의>
```
mongoDB 인스턴스 1개는 독립적인 여러 개의 데이터 베이스를 만들 수 있다.
```python
# 컬렉션 얻기
<컬렉션 참조 변수> = db.<컬렉션 이름 사용자 정의>
```
컬렉션은 도큐먼트들의 집합으로 데이터베이스 안에 존재한다. 여러 형태의 도큐먼트를 하나의 컬렉션 안에 대입할 수 있다.
```python
# 도큐먼트 정의
<도큐먼트 이름 사용자 정의> = {} 
```
몽고DB는 JSON 스타일로 저장되므로 파이썬에서는 딕셔너리를 활용해 이를 표현한다.
```python
# 도큐먼트 삽입
도큐먼트_id = <컬렉션 참조 변수>.insert(<도큐먼트 이름>)
```
컬렉션과 DB는 도큐맨트를 1개 이상 삽입해서야 그때서야 생성된다. 도큐먼트_id는 별도 지정하지 않으면 자동 생성되고 지정할 경우 도큐먼트 마다 구별하기 위해서 유니크해야한다.
##### - read
```python
# 컬렉션에서 도큐먼트 얻어오기 
<컬렉션 참조 변수>.find_one(<선택 기준(query)>)
```
find_one() 함수는 요청에 맞는 하나의 도큐먼트만 가져오고 싶을 때 쓰는 함수이다. 선택 기준에는 도큐먼트의 key-value나 _id가 될수 있다. 또한 쿼리 비교 연산자를 사용하여 더 확장된 쿼리를 쓸 수 있다.</br></br>
비교 연산자\
<img src="image/compare.png" width="600" height="330">
```python
<컬렉션 참조 변수>.find(<선택 기준(query)>)
```
find() 함수를 통하면 한개 이상의 도큐먼트를 위한 쿼리를 요청할 수 있다. 또한 find()는 cuser instance를 반환하는데 이것은 도큐먼트들을 순회할 수 있도록 해준다. 그래서 for 문과 결합하여 사용할 수 있다.
```python
<컬렉션 참조 변수>.count()
<컬렉션 참조 변수>.find(<선택 기준(query)>).count()
```
도큐먼트의 전체 개수나 쿼리에 매칭되는 도큐먼트의 개수를 구할 경우 count() 함수를 통해서 알 수 있다.
```python
<데이터베이스 참조 변수>.connection_names()
```
<정의한 데이터베이스에> 어떤 컬렉션들이 존재하는지 리스트를 학인할 수 있다.
##### - update
```python
<컬렉션 참조 변수>.update(<선택 key-value>,<변경 key-value>)
```
컬렉션에서 선택 key-value인 키와 값에 대해서 변경 key-value로 업데이트가 된다.
##### - delete 
```python
<컬렉션 참조 변수>.remove(<선택 기준 key-value>)
```
선택 기준에 사용되는 key와 value에 대해서 delete한다.

### Reference
- https://poiemaweb.com/mongdb-basics-shell-crud
- https://ngee.tistory.com/335
- https://ngee.tistory.com/336
- https://ngee.tistory.com/339
- https://ngee.tistory.com/340
