from flask import Flask, request, jsonify, render_template, session, redirect, url_for, escape
import os, json, threading, time
import pandas as pd
import numpy as np
from datetime import datetime
from connectDatabase import ConnectDatabase
import random

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')

@app.route("/saveLectures", methods=["POST"])
def saveLectures():
    session["lectures"] = request.get_json()["lectures"]
    return {"message": "ok"}

@app.route("/getQuestions", methods=["GET"])
def getQuestions():
    if len(session["lectures"]) == 1:
        stringLectures = str(tuple(session["lectures"]))[:-2] + ")"
    else:
        stringLectures = str(tuple(session["lectures"]))
    query_str = "SELECT DISTINCT question, imageQuestion FROM qldapm_table WHERE lecture IN " + stringLectures
    connectDatabase = ConnectDatabase()
    allQuestionsInLecture = connectDatabase.cursor.execute(query_str).fetchall()
    data = []
    for row in allQuestionsInLecture:
        question = row.question
        imageQuestion = row.imageQuestion
        query_str = "SELECT answer, imageAnswer, isCorrect FROM qldapm_table WHERE question = ? AND imageQuestion = ? AND lecture IN " + stringLectures
        questions = connectDatabase.cursor.execute(query_str, question, imageQuestion).fetchall()
        answer = []
        for q in questions:
            answer.append({"answer": q.answer, "imageAnswer": q.imageAnswer, "isCorrect": q.isCorrect})
        random.shuffle(answer)
        data.append({"question": question, "imageQuestion": imageQuestion, "answer": answer})
        random.shuffle(data)
    return app.response_class(json.dumps(data), mimetype='application/json')


@app.route("/hoc", methods=["GET"])
def learn():
    return render_template('learn.html')

if __name__ == "__main__":
    app.run(debug=True)