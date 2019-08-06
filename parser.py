import json
import re
import constants
import pprint
from datetime import datetime, timezone, timedelta
import time

global major_documents
global essential_documents
global selective_documents

def json_file_to_dict(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def check_overlap_document(documents):
    for document in documents:
        count = 0
        for check_document in documents:
            if document["과목번호"] == check_document["과목번호"]:
                count += 1
        for i in range(2, constants.OVERLAP_MAX):
            if count == i:
                print("중복 과목:", document["과목번호"], "중복 횟수:", i)
                break


def jsontime_to_timestamp(jsonday, jsontime):
    """
    :param jsonday: 월 화 수 목 금 토
    :param jsontime: 15:00-16:15
    :return :
    """
    date = "2019-07-" + constants.STR2STRINGNUMBER[jsonday]
    start_time = date + " " + jsontime[0:2] + ":" + jsontime[3:5] + ":" + "00"
    start_time_stamp = time.mktime(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timetuple())
    end_time = date + " " + jsontime[6:8] + ":" + jsontime[9:11] + ":" + "00"
    end_time_stamp = time.mktime(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timetuple())

    return [start_time_stamp, end_time_stamp]
    # return str(start_time_stamp) + "-" + str(end_time_stamp)


def set_lecture_time(documents):
    """
    :param documents:
    :return documents added time field:
    """
    for document in documents:
        time_location_split = document["강의시간(강의실)"].split("\n")
        _new_times = []
        for time_location in time_location_split:
            m = re.search(r"(?P<days>[월화수목금토 ]*) (?P<time>\d{2}:\d{2}-\d{2}:\d{2}) \((.*)", time_location)
            if m is not None:
                for day in m.group("days").split(" "):
                    ts = jsontime_to_timestamp(day, m.group("time"))
                    should_append = True
                    for _new_time in _new_times:
                        time_diff = abs(ts[0] - _new_time[1]) / 60
                        if time_diff < 30:
                            _new_time[1] = ts[1]
                            should_append = False
                        if ts[0] - _new_time[0] == 0 or ts[1] - _new_time[1] == 0:
                            should_append = False
                    if should_append:
                        _new_times.append(ts)

        document["time"] = _new_times

    return documents  # 시간 필드 생성하고 리턴


def major_parse(file_path, year, semester):
    """
    :param file_path:
    :param year:
    :param semester:
    :return 몽고DB에 저장할 Document 형태의 전공 리스트를 반환:
    """
    parsed_data = json_file_to_dict(file_path)[year][semester]
    ret = []

    for college in parsed_data.keys():
        for faculty in parsed_data[college].keys():
            for major in parsed_data[college][faculty].keys():
                for document in parsed_data[college][faculty][major]:
                    document["이수구분(주전공)"] = document["이수구분(주전공)"].split()
                    document.update({'year': year, 'semester': semester})
                    ret.append(document)

    ret = set_lecture_time(ret)
    # check_overlap_document(ret)  # 중복 과목 체크 코드
    return ret


def essential_parse(file_path, year, semester):
    """
    :param file_path:
    :param year:
    :param semester:
    :return 몽고DB에 저장할 Document 형태의 교필 리스트를 반환:
    """
    parsed_data = json_file_to_dict(file_path)[year][semester]
    ret = []

    for grade in parsed_data.keys():
        for class_name in parsed_data[grade].keys():
            for document in parsed_data[grade][class_name]:
                document.update({'year': year, 'semester': semester})
                ret.append(document)

    # ret = set_lecture_time(ret)
    check_overlap_document(ret) # 중복 과목 체크 코드
    return ret


def selective_parse(file_path, year, semester):
    """
    :param file_path:
    :param year:
    :param semester:
    :return 몽고DB에 저장할 Document 형태의 교선 리스트를 반환:
    """
    parsed_data = json_file_to_dict(file_path)[year][semester]
    ret = []  # 교선 교과목 리스트(딕셔너리 리스트)

    for domain in parsed_data:
        for document in parsed_data[domain]:
            document.update({'year': year, 'semester': semester})
            ret.append(document)

    # ret = set_lecture_time(ret)
    # check_overlap_document(document_list) # 중복 과목 체크 코드
    return ret


test_data = [
    {
        "계획": " ",
        "이수구분(주전공)": "전선-컴퓨터",
        "이수구분(다전공)": "복선-컴퓨터",
        "공학인증": " ",
        "교과영역": " ",
        "과목번호": "2150059401",
        "과목명": "[심화]Co-op SAP 트랙(캡스톤디자인)",
        "분반": " ",
        "교수명": "홍지만\n장의진\n홍지만\n장의진",
        "개설학과": "스파르탄 SW교육원",
        "시간/학점(설계)": "6.00 /6.0",
        "수강인원": "0",
        "여석": "0",
        "강의시간(강의실)": "월 화 수 목 18:30-19:45 (전산관 19328 - 첨단PC실습실-홍지만)\n월 화 수 목 18:30-19:45 (전산관 19328 - 첨단PC실습실-장의진)\n월 화 수 목 20:00-21:15 (전산관 19328 - 첨단PC실습실-홍지만)\n월 화 수 목 20:00-21:15 (전산관 19328 - 첨단PC실습실-장의진)",
        "수강대상": "3학년 컴퓨터 ,소프트 ,스마트시스템소프트 ,글로벌미디어\n4학년 컴퓨터 ,소프트 ,스마트시스템소프트 ,글로벌미디어"
    },
    {
        "계획": " ",
        "이수구분(주전공)": "전선-컴퓨터",
        "이수구분(다전공)": "복선-컴퓨터",
        "공학인증": " ",
        "교과영역": " ",
        "과목번호": "2150059601",
        "과목명": "[심화]Co-op실감형게임콘텐츠개발트랙(캡스톤디자인)",
        "분반": " ",
        "교수명": "성정환\n성정환",
        "개설학과": "스파르탄 SW교육원",
        "시간/학점(설계)": "6.00 /6.0",
        "수강인원": "0",
        "여석": "0",
        "강의시간(강의실)": "월 화 수 목 12:00-13:15 (전산관 19328 - 첨단PC실습실-성정환)\n월 화 수 목 13:30-14:45 (전산관 19328 - 첨단PC실습실-성정환)",
        "수강대상": "3학년 컴퓨터 ,소프트 ,스마트시스템소프트 ,글로벌미디어\n4학년 컴퓨터 ,소프트 ,스마트시스템소프트 ,글로벌미디어"
    },
]

ret = set_lecture_time(test_data)
KST = timezone(timedelta(hours=9))

for r in ret:
    print(r["과목명"])
    _times = r["time"]
    for _time in _times:
        print("{} - {}".format(
            datetime.fromtimestamp(_time[0], KST).strftime("%Y/%m/%d %H:%M"),
            datetime.fromtimestamp(_time[1], KST).strftime("%Y/%m/%d %H:%M")
        ))

# major_documents = major_parse("./data/majors.json", "2019", "2 학기")
# essential_documents = essential_parse("./data/essentials.json", "2019", "2 학기")
# selective_documents = selective_parse("./data/selectives.json", "2019", "2 학기")

    # pprint.pprint(major_documents)
    # pprint.pprint(essential_documents)
    # pprint.pprint(selective_documents)
