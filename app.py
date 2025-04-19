from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

# Чтение JSON-ключа из переменной окружения GOOGLE_CREDENTIALS
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# Подключение к Google Sheets
zayavki_sheet = client.open("Контейнер Склад").worksheet("zayavki")

# Flask-приложение
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    kto = request.form["kto"]
    code = request.form["code"]
    name = request.form["name"]
    count = request.form["count"]
    comment = request.form["comment"]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    zayavki_sheet.append_row([timestamp, kto, code, name, count, comment, "Ожидает"])

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))