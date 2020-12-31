from flask import Flask, request, jsonify, render_template, session, redirect, url_for, escape
import os, json, threading, time
import pandas as pd
import numpy as np
from datetime import datetime
from connectDatabase import ConnectDatabase


query_str = "SELECT COUNT(DISTINCT question) FROM qldapm_table WHERE lecture IN " + str(tuple(['Bài 5: Ước lượng dự án và xây dựng ngân sách (dự toán) ', 'Bài 08: Quản lý phát triển, tổ chức dựa án và nguồn nhân lực']))
print(query_str)
connectDatabase = ConnectDatabase()

print(connectDatabase.cursor.execute(query_str ).fetchval())
