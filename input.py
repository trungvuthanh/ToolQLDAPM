from connectDatabase import ConnectDatabase
import pandas as pd
import numpy as np
import io, math

QLDAPM = pd.read_excel("QLDAPM.xlsx")
g = io.open("qldapm.sql", mode="w", encoding="utf-8")
g.write("DROP DATABASE IF EXISTS QLDAPM_DB; \nCREATE DATABASE QLDAPM_DB; \nCREATE TABLE qldapm_table (\n\tid int(11) PRIMARY KEY AUTO_INCREMENT, \n\tlecture VARCHAR(255), \n\tquestion TEXT, \n\timageQuestion VARCHAR(255), \n\tanswer TEXT, \n\timageAnswer VARCHAR(255), \n\tisCorrect VARCHAR(255) \n); \nINSERT INTO qldapm_table (lecture, question, imageQuestion, answer, imageAnswer, isCorrect) VALUES \n")

(lecture, question, imageQuestion) = ("", "", "")
rowi = -1
for i, row in QLDAPM.iterrows():
    if row["key"] == "T": 
        rowi += 1
        lecture = row["content"]
    elif row["key"] == "H": 
        question = row["content"]
        imageQuestion = "" if math.isnan(row["image"]) else "/static/image/" + str(int(row["image"])) + ".png"
    elif row["key"] == "end":
        g.write(";")
    else:
        isCorrect = "true" if row["key"] == "Đ" else "false"
        imageAnswer = "" if math.isnan(row["image"]) else "/static/image/" + str(int(row["image"]))
        answer = str(row["content"])
        if rowi != 0:
            g.write(",\n")
        g.write("(\"" + lecture + "\", \"" + question + "\", \"" + imageQuestion + "\", \"" + answer + "\", \"" + imageAnswer + "\", \"" + isCorrect + "\")")
        rowi += 1
g.close()
print()