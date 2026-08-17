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
def intake(tracking_number: str = Form(...)):
    date_logged = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    connection = sqlite3.connect("packages.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO packages (tracking_number, date_logged, status) VALUES (?, ?, ?)", 
        (tracking_number, date_logged, "pending")
    )
    connection.commit()

    return {"tracking number": tracking_number}