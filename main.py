from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates



app = FastAPI()

# tell Jinja2 which folder to look in
templates = Jinja2Templates(directory= "templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/intake")
def intake(tracking_number: str = Form(...)):
    return {"tracking number": tracking_number}