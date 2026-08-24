from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from datetime import datetime
import sqlite3


app = FastAPI()

# tell Jinja2 which folder to look in
templates = Jinja2Templates(directory= "templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/intake")
def intake(tracking_number: str = Form(...), recipient_name: str = Form(...)):
    date_logged = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    connection = sqlite3.connect("packages.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO packages (tracking_number, recipient_name, date_logged, status) VALUES (?, ?, ?, ?)", 
        (tracking_number, recipient_name, date_logged, "pending")
    )
    connection.commit()
    return {"tracking number": tracking_number}

@app.get("/lookup")
def lookup(tracking_number: str):
    connection = sqlite3.connect("packages.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM packages WHERE tracking_number = ?", 
                    (tracking_number,)
    )
    result = cursor.fetchone()

    if result:
        return {"ID": result[0], "Recipient Name" : result[2]}
    else:
        return "Tracking number not found"
