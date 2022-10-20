import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from DataModel import DataModel
from PredictionModel import PredictionModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

pred_model = PredictionModel()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "BASE_URL": os.getenv("BASE_URL", "http://localhost:8000/")
    })


@app.post("/comment/predict")
def ask_prediction(data: DataModel):
    return pred_model.make_predictions(data)
