import pandas as pd

from treinamento_xgboost import model, X

df_prof = pd.read_csv("features.csv")

df_prof = df_prof[X.columns]

pred = model.predict(df_prof)[0]

classes = {
    0: "NASCIMENTO NOVA",
    1: "CASAMENTO NOVA",
    2: "NASCIMENTO ANTIGA",
    3: "CASAMENTO ANTIGA"
}

print("Classificação:", classes[pred])