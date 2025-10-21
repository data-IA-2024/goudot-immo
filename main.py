from typing import Union
from typing_extensions import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import mlflow
import pandas as pd

mlflow.set_tracking_uri(uri='http://localhost:5000')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

model=None

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"name": "Appli ML"})


@app.post("/predict")
def read_item(request: Request, local: Annotated[str, Form()], pieces:Annotated[int, Form()], terrain:Annotated[int, Form()], surface_total:Annotated[int, Form()]):
    global model
    data = pd.DataFrame({
        "local": [local],
        "pieces": [pieces],
        "terrain": [terrain],
        "surface_total": [surface_total],
    })
    if not model:
        return "Pas de modèle chargé !"
    predict = model.predict(data)
    #return f"OK {local=} {pieces=} {terrain=} {surface_total=} => {predict}"
    return templates.TemplateResponse(request=request, name="result.html", context={"local":local, "predict": predict[0]})

@app.get("/update")
def update_model(id: str):
    global model
    model = mlflow.pyfunc.load_model(id)
    return f"OK, loaded {id}"