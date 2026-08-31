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
def intake(tracking_number: str = Form(...), recipient_name: str = Form(...), package_type: str = Form(...)):
    date_logged = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    connection = sqlite3.connect("packages.db")
    cursor = connection.cursor()
    try:
        cursor.execute(
                "INSERT INTO packages (tracking_number, recipient_name, package_type, date_logged, status) VALUES (?, ?, ?, ?, ?)", 
                (tracking_number, recipient_name, package_type, date_logged, "pending")
            )
        connection.commit()
        package_id = cursor.lastrowid
        

    except Exception as e:
        return {"error": str(e)}
    finally:
        connection.close()

    return {"package_id" : package_id, "recipient_name": recipient_name, "package_type": package_type,"tracking_number": tracking_number}

@app.get("/lookup")
def lookup(search_input: str):
    connection = sqlite3.connect("packages.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM packages WHERE (tracking_number LIKE ? OR recipient_name LIKE ?) AND status = ?", 
                            (f"%{search_input}%", f"%{search_input}%", "pending")
            )
        result = cursor.fetchall()
    except Exception as e:
        result = None
    finally:
        connection.close()
    if result:
        res = []
        # result returns a list of rows
        # for loop converts each row into a dict that gets returned
        for el in result:
            res.append(dict(el))
        return res
    else:
        return "Tracking number not found"

@app.post("/pickup")
def pickup(tracking_number: str = Form(...)):
    date_picked_up = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    connection = sqlite3.connect("packages.db")
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE packages SET status = ?, date_picked_up = ? WHERE tracking_number = ?", 
                           ("picked up", date_picked_up, tracking_number,)
            )
        if cursor.rowcount == 0:
            raise Exception("No matching tracking number found")
        connection.commit()
    except Exception as e:
        return {"error" : str(e)}
    finally:
        connection.close()
    return {"tracking number:" : tracking_number, "picked up": "has been picked up"}