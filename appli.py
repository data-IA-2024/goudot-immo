import mlflow
import pandas as pd

mlflow.set_tracking_uri(uri='http://localhost:5000')

logged_model = 'runs:/b383e867adba4fac8a4fcb68ac7b8583/model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on a Pandas DataFrame.
#data=[[ 'Maison',     4.0,      0.0,          83.72]]
df=pd.read_csv("data/ValeursAll.csv")
features="local,pieces,terrain,surface_total".split(',') # ,prixm2
X = df[features]

y = loaded_model.predict(X)
print(y)