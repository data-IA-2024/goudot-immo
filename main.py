from typing import Union
from typing_extensions import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import mlflow
import pandas as pd
from prometheus_fastapi_instrumentator import Instrumentator

mlflow.set_tracking_uri(uri='http://localhost:5000')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

Instrumentator().instrument(app).expose(app, include_in_schema=False) # expose /metrics

model=None

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"name": "Appli ML"})

@app.get("/health")
def get_health(request: Request):
    return "OK"

@app.post("/predict")
def read_item(request: Request, local: Annotated[str, Form()], pieces:Annotated[int, Form()], terrain:Annotated[int, Form()], surface_total:Annotated[int, Form()], insee:Annotated[str, Form()]):
    global model

    data = pd.DataFrame({
        "local": [local],
        "pieces": [pieces],
        "terrain": [terrain],
        "surface_total": [surface_total],
        #"taille_unite_urbaine":df_commune.loc['41017','taille_unite_urbaine'],
    })
    for col in cols_communes[1:]:
        data[col] = float(df_commune.loc[insee, col])

    if not model:
        return "Pas de modèle chargé !"
    predict = model.predict(data)
    #return f"OK {local=} {pieces=} {terrain=} {surface_total=} => {predict}"
    return templates.TemplateResponse(request=request, name="result.html", context={"local":local, "predict": round(predict[0],2)})

@app.get("/update")
def update_model(id: str):
    # runs:/fd0c453e958a4fb89ba5fc0fd0c8cb45/model
    # models:/model_test/latest
    global model
    model = mlflow.pyfunc.load_model(id)
    return f"OK, loaded {id}"