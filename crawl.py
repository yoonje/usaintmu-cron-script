import pysaint

res = pysaint.get("전공", 2019, "2 학기", silent=True)
pysaint.save_json("./data", "majors.json", res["2019"]["2 학기"])

res = pysaint.get("교양필수", 2019, "2 학기", silent=True)
pysaint.save_json("./data", "essentials.json", res["2019"]["2 학기"])

res = pysaint.get("교양선택", 2019, "2 학기", silent=True)
pysaint.save_json("./data", "selectives.json", res["2019"]["2 학기"])