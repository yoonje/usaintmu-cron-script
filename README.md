# Soongsil University Timetable Appliction Server
숭실대 수강신청 정보를 전송을 통한 시간표 제작 앱의 장고 서버입니다. pysaint와 pymongo를 사용한 cron script을 통해서 수강신청 정보를 잦은 주기로 MongoDB에 저장하여 장고를 통해 최신의 정보를 사용자에게 전달합니다.

### Version
- Python: 3.6.8
- MongoDB: 3.4.0
- pymongo: 3.8.0
- pysaint: 1.5.2
### Installation

```sh
$ sudo pip install -r requirements.txt
```


### To Run App
```sh
$ ./manage.py runserver or python3 manage.py runserver
```

### MongoDB Document Shape

JOSN 파일에 년도와 학기에 해당하는 키를 추가했고 이수구분 키들의 값을 리스트로 변경했습니다.

ex) 

```js
document = {
    "계획": " ",
    "이수구분(주전공)": ["전선-기독교"],
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
    "년도": "2017",
    "학기": "2 학기" 
}
```