import mlflow
import pandas as pd

mlflow.set_tracking_uri(uri='http://localhost:5000')

logged_model = 'runs:/04d1b9985ba34c1ab9fa0c750ab6312d/model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

data = pd.DataFrame({
    "local": ['Maison', 'Appartement'],
    "pieces": [4, 2],
    "terrain": [100, 0],
    "surface_total": [100, 50],
})

y = loaded_model.predict(data)
print(y)