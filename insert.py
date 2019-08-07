from mongoengine import *
import parser as ps
import constants
from datetime import datetime, timezone, timedelta

connect('usaintmu_db')


class Time(EmbeddedDocument):
    start_time = DateTimeField()
    end_time = DateTimeField()


class Lecture(Document):
    semester = StringField()
    time = ListField(EmbeddedDocumentField('Time'))
    year = StringField()
    time_location = StringField()
    department = StringField()
    plan = StringField()
    engineering_certification = StringField()
    subject_name = StringField()
    subject_code = StringField(required=True)
    subject_area = StringField()
    professor = StringField()
    division_class = StringField()
    course_target = StringField()
    number_of_student = StringField()
    time_unit = StringField()
    remaining_seat = StringField()
    division_multiple = StringField()
    division_prime = ListField(StringField())


def transform_db_key(documents):
    ret = []
    for _document in documents:
        englishDict = dict()
        for k in _document.keys():
            englishDict[constants.key_converter[k]] = _document[k]
        ret.append(englishDict)
    return ret


def save_documnet(document):
    lec = Lecture()
    lec.semester = document["semester"]
    lec.year = document["year"]
    lec.time_location = document["time_location"]
    lec.department = document["department"]
    lec.plan = document["plan"]
    lec.engineering_certification = document["engineering_certification"]
    lec.subject_name = document["subject_name"]
    lec.subject_code = document["subject_code"]
    lec.subject_area = document["subject_area"]
    lec.professor = document["professor"]
    lec.division_class = document["division_class"]
    lec.course_target = document["course_target"]
    lec.number_of_student = document["number_of_student"]
    lec.time_unit = document["time_unit"]
    lec.remaining_seat = document["remaining_seat"]
    lec.division_multiple = document["division_multiple"]
    lec.division_prime = document["division_prime"]

    for i in range(0, len(document["time"])):
        time = Time(start_time=datetime.fromtimestamp(document["time"][i]["start_time"], constants.KST),
                    end_time=datetime.fromtimestamp(document["time"][i]["end_time"]))
        lec.time.append(time)

    return lec


# 전공은 주전공 이수구분에 따라서 중복이 생기므로 처리 해줘야함(이수구분(주전공) plus and not insert)
def save_major_document(documents):
    db_documents = transform_db_key(documents)

    for _document in db_documents:
        lec = save_documnet(_document)

        if Lecture.objects(subject_code=lec.subject_code):
            temp_lec = Lecture.objects.get(subject_code=lec.subject_code)
            temp_lec.division_prime = temp_lec.division_prime.extend(_document["division_prime"])
            temp_lec.save()
        else:
            lec.save()


def save_essential_document(documents):
    db_documents = transform_db_key(documents)

    for _document in db_documents:
        lec = save_documnet(_document)
        lec.save()


# 교선은 교과영역에 따라서 중복이 생기므로 처리해줘야함(not insert)
def save_selective_document(documents):
    db_documents = transform_db_key(documents)

    for _document in db_documents:
        lec = save_documnet(_document)
        if Lecture.objects(subject_code=lec.subject_code):
            pass
        else:
            lec.save()


if __name__ == "__main__":
    save_major_document(ps.major_documents)
    # save_essential_document(ps.essential_documents)
    # save_selective_document(ps.selective_documents)
