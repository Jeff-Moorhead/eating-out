from flask import Flask, render_template, request
from datetime import datetime
import os
import psycopg2

app = Flask("eatingout")
DATABASE = os.environ['DATABASE_URL']

INSERT_SQL = """\
    INSERT INTO meal (mealdate, location, cost, name)
    VALUES (?, ?, ?, ?);
    """

MEALS_SQL = """\
    SELECT mealdate, location, cost, name FROM meal
    WHERE date >= ? and date <= ?;
    """

CREATE_SQL = """\
    CREATE TABLE IF NOT EXISTS meal (
        mealdate date,
        location text,
        cost real,
        name text,
        PRIMARY KEY (mealdate, location, name)
    );
    """


def get_db():
    db = psycopg2.connect(DATABASE, sslmode='require')
    return db


def get_first_day(date):
    return datetime(year=date.year, month=date.month, day=1)


@app.route("/")
def index():
    today = datetime.today()
    first_day = get_first_day(today)
    db = get_db()
    cur = db.cursor()
    rows = cur.execute(MEALS_SQL, [first_day, today]).fetchall()
    db.close()
    return render_template("index.html", today=today.strftime("%Y-%m-%d"), meals=rows)


@app.route("/addmeal", methods=["POST"])
def addmeal():
    date = request.form['date']
    location = request.form['location']
    cost = request.form['cost']
    name = request.form['name']
    db = get_db()
    db.execute(INSERT_SQL, [date, location, cost, name])
    db.commit()
    db.close()
    return render_template("addmeal.html", date=date, location=location, cost=cost, name=name)


if __name__ == "__main__":
    app.run(debug=True)
