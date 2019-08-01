import json
import itertools
import constants
from pprint import *


def json_file_to_dict(file_path):
    with open(file_path, "r") as f:
        dict = json.load(f)
    return dict


def check_overlap_document(document_list):
    # 중복 과목 체크
    for document in document_list:
        count = 0
        for check_document in document_list:
            if document["과목번호"] == check_document["과목번호"]:
                count += 1
        for i in range(2, constants.OVERLAP_MAX):
            if count == i:
                print("중복 과목:", document["과목번호"], "중복 횟수:", i)
                break


def major_parse(file_path, year, semester):
    '''
    :param file_path:
    :param year:
    :param semester:
    :return 몽고DB에 저장할 Document 형태의 전공 리스트를 반환:
    '''
    major_dict = json_file_to_dict(file_path)
    college_list = list(major_dict[year][semester].keys())  # 학부 리스트
    department_list = []  # 학과 리스트(2차원 리스트)
    document_list = []  # 전공 교과목 리스트(딕셔너리 리스트)

    for college in college_list:
        department_list.append(list(major_dict[year][semester][college].keys()))

    for i, college_department in enumerate(department_list):
        college = college_list[i]
        for department in college_department:
            document_list.append(list(major_dict[year][semester][college][department].values()))

    document_list = list(itertools.chain(*document_list))  # iterator.chain() : 3차원 리스트 -> 2차원 리스트
    document_list = list(itertools.chain(*document_list))  # iterator.chain() : 2차원 리스트 -> 1차원 리스트

    check_overlap_document(document_list)  # 중복 과목 체크 코드

    for document in document_list:
        document["년도"] = year
        document["학기"] = semester
        document["이수구분(다전공)"] = document["이수구분(다전공)"].split("/")

    return document_list


def essential_parse(file_path, year, semester):
    '''
    :param file_path:
    :param year:
    :param semester:
    :return 몽고DB에 저장할 Document 형태의 교필 리스트를 반환:
    '''
    essential_dict = json_file_to_dict(file_path)
    grade_list = list(essential_dict[year][semester].keys())  # 학년 리스트
    document_list = []  # 교필 교과목 리스트(딕셔너리 리스트)

    for grade in grade_list:
        document_list.append(essential_dict[year][semester][grade].values())

    document_list = list(itertools.chain(*document_list))  # iterator.chain() : 3차원 리스트 -> 2차원 리스트
    document_list = list(itertools.chain(*document_list))  # iterator.chain() : 2차원 리스트 -> 1차원 리스트

    # check_overlap_document(document_list) #중복 과목 체크 코드

    for document in document_list:
        document["년도"] = year
        document["학기"] = semester
        document["이수구분(다전공)"] = document["이수구분(다전공)"].split("/")

    return document_list


def selectives_parse(file_path, year, semester):
    '''
    :param file_path:
    :param year:
    :param semester:
    :return 몽고DB에 저장할 Document 형태의 교선 리스트를 반환:
    '''
    selectives_dict = json_file_to_dict(file_path)
    domain_list = list(selectives_dict[year][semester].keys())  # 구분 영역 리스트(전체, 15이전, 16-18...)
    document_list = []  # 교선 교과목 리스트(딕셔너리 리스트)

    for domain in domain_list:
        document_list.append(selectives_dict[year][semester][domain])

    document_list = list(itertools.chain(*document_list))  # iterator.chain() : 2차원 리스트 -> 1차원 리스트

    # check_overlap_document(document_list) #중복 과목 체크 코드

    for document in document_list:
        document["년도"] = year
        document["학기"] = semester
        document["교과영역"] = document["교과영역"].split("\n")

    return document_list


major_documents = major_parse("./data/majors.json", "2019", "2 학기")
essential_documents = essential_parse("./data/essentials.json", "2019", "2 학기")
selectives_documents = selectives_parse("./data/selectives.json", "2019", "2 학기")
documents = major_documents + essential_documents + selectives_documents
