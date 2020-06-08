# Usaintmu Cron Script
숭실대 수강신청 정보의 전송을 위해 [pysaint](https://github.com/gomjellie/pysaint)와 pymongo를 사용하여 cron script를 작성하고 설정된 주기에 따라 MongoDB에 저장합니다. 이후 웹 애플리케이션을 통해 변경된 최신 수강 신청 정보를 사용자에게 전달할 수 있습니다.

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
crawl.py 안에서 과목 구분, 연도, 학기를 선택할 수 있습니다.
```sh
$ python3 crawl.py
```
```sh
$ python3 parser.py
```
`usaintmu_db`라고 MongoDB 컬렉션을 만들고 insert.py를 실행하세요.
```sh
$ python3 insert.py
```


### Document Schema
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

### 유상무 Store
- https://play.google.com/store/apps/details?id=com.usaintmu&hl=ko
- https://apps.apple.com/kr/app/%EC%9C%A0%EC%83%81%EB%AC%B4/id1476194177
