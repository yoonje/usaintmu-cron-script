import json
import re
import constants
import pprint


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


def set_lecture_time(documents):
    for document in documents:
        time_location_split = document["강의시간(강의실)"].split("\n")
        for time_location in time_location_split:
            m = re.search(r"(?P<day>[월화수목금토 ]+) (?P<time>\d{2}:\d{2}-\d{2}:\d{2}) \((.* [\da-zA-Z]+)-(\D+)\)", time_location) # 정규식에 문제가 있음
            if m is None:
                document["time"] = "\xa0"
            else:
                document["time"] = m.group("day") + m.group("time")
        pprint.pprint(document)


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

    # check_overlap_document(document_list) #중복 과목 체크 코드
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

    # check_overlap_document(document_list) #중복 과목 체크 코드
    return ret


if __name__ == "__main__":
    major_documents = major_parse("./data/majors.json", "2019", "2 학기")
    essential_documents = essential_parse("./data/essentials.json", "2019", "2 학기")
    selective_documents = selective_parse("./data/selectives.json", "2019", "2 학기")

    set_lecture_time(major_documents)
    # pprint.pprint(major_documents)
    # pprint.pprint(essential_documents)
    # pprint.pprint(selective_documents)
