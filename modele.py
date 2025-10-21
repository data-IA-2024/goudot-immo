import sys, glob
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import mlflow, mlflow.sklearn

fns=glob.glob('data/ValeursFoncieres*.csv')

dept = '31'

print(fns)
dfs=[pd.read_csv(fn) for fn in fns]

df = pd.concat(dfs, ignore_index=True)
#print(df)
print(df.dtypes)

df.to_csv("data/ValeursAll.csv", index=False)
#print(df.code_dept)
df=df[df['code_dept']==dept]
#print(df)

features="local,pieces,terrain,surface_total".split(',') # ,prixm2
target = 'valeur' # 'prixm2'
print('features', features)
X = df[features]
y = df[target]

print(X)

#print('correlations avec y')
#print(df[features].corrwith(y))

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Définition des colonnes numériques
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = ['local']  # Colonne catégorielle
#print('numeric_features', numeric_features)

# Pipeline de prétraitement
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
# Pipeline pour les colonnes catégorielles
categorical_transformer = Pipeline(steps=[
    #('imputer', SimpleImputer(strategy='most_frequent')),  # Remplace les valeurs manquantes par la valeur la plus fréquente
    ('onehot', OneHotEncoder(handle_unknown='ignore'))  # Encode les catégories en variables binaires
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Pipeline complet avec le modèle
regressor = RandomForestRegressor(n_estimators=100) # , random_state=42

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', regressor)
])

mlflow.set_tracking_uri(uri='http://localhost:5000')
mlflow.set_experiment(f"goudot-p4-RF")

with mlflow.start_run() as run:
    # Exécuter la recherche sur les données d'entraînement
    model.fit(X_train, y_train)
    #grid_search.fit(dtrain)

    y_pred = model.predict(X_test)

    # Calcule le score R²
    r2 = r2_score(y_test, y_pred)

    # Enregistrer les paramètres et métriques
    mlflow.log_params({"code_dept": dept})
    mlflow.log_params({"df_shape": df.shape})
    mlflow.log_metric("r2_score", r2)  # Enregistre le score R²
    print(f"{r2=:.3f}")

    mlflow.sklearn.log_model(model, "model")
