import sqlite3
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

subjects = {}

@app.route("/")
def index():
    with sqlite3.connect("portfolio.db") as db:
        temp = db.execute("SELECT * FROM SUBJECTS").fetchall() # List of tuples
    
    for s in temp:
        perc = 0
        with sqlite3.connect("portfolio.db") as db:
            temp1 = db.execute("SELECT complete FROM TOPICS where subject_id = ?", [s[0]]).fetchall()

        for t in temp1:
            perc += t[0]
        try:
            perc = perc / len(temp1) * 100
            perc=round(perc)
        except:
            perc = 0
            
        subjects[s[1]] = perc
    
    return render_template("index.html", subjects=subjects)

@app.route("/complete", methods=["POST"])
def complete():

    try: 
        topic = request.form.get("topic")
        subject = request.args.get("subject")
        with sqlite3.connect("portfolio.db") as db:
            db.execute("UPDATE TOPICS SET complete = 1 WHERE Topic = ?", [topic])
        return redirect(f"/subjects?subject={subject}")
    except:
        pass

    return redirect("/")

@app.route("/uncomplete", methods=["POST"])
def Uncomplete():

    try: 
        topic = request.form.get("topic")
        subject = request.args.get("subject")
        with sqlite3.connect("portfolio.db") as db:
            db.execute("UPDATE TOPICS SET complete = 0 WHERE Topic = ?", [topic])
        return redirect(f"/subjects?subject={subject}")
    except:
        pass

    return redirect("/")

@app.route("/subjects")
def Subjects(): 
    subject = request.args.get("subject")

    match subject:
        case "Programming":
            id = "prog"
        case "Discrete Mathematics":
            id = "discrete"
        case "Data Structures and Algorithms":
            id = "data_structs"
        case "Web Development":
            id = "webdev"
        case "Databases":
            id = "databases"
        case "Computer Networks and Security":
            id = "networks"
        case "Cloud Software Development":
            id = "cloud"
        case "Mobile App Development":
            id = "mobile"
        case "Data Analysis":
            id = "data_analysis"

    print(id)

    with sqlite3.connect("portfolio.db") as db:
        temp = db.execute("SELECT Topic, Complete FROM TOPICS WHERE subject_id = ?", [id])
    topics = {}
    for t in temp:
        topics[t[0]] = t[1]

    return render_template(f"subjects/general.html", topics=topics, subject=subject)  


