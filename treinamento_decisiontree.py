import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# ======================================================
# 1) Carregando as features
# ======================================================

features1 = pd.read_csv('features1.csv')
features2 = pd.read_csv('features2.csv')
features3 = pd.read_csv('features3.csv')
features4 = pd.read_csv('features4.csv')

# Removendo colunas desnecessárias
features1 = features1.drop(['texto_raw', 'texto_normalizado'], axis=1)
features2 = features2.drop(['texto_raw', 'texto_normalizado'], axis=1)
features3 = features3.drop(['texto_raw', 'texto_normalizado'], axis=1)
features4 = features4.drop(['texto_raw', 'texto_normalizado'], axis=1)

# ======================================================
# 2) Labels
# ======================================================

features1['label'] = 0
features2['label'] = 1
features3['label'] = 2
features4['label'] = 3

# ======================================================
# 3) Concatenando
# ======================================================

features_completas = pd.concat([features1, features2, features3, features4])
features_completas = features_completas.set_index('nome_arquivo')

X = features_completas.drop(columns=['label'])
y = features_completas['label']

# ======================================================
# 4) Divisão treino/teste
# ======================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ======================================================
# 5) Decision Tree (não precisa normalizar)
# ======================================================

model = DecisionTreeClassifier(
    criterion="gini",
    max_depth=None,            # pode crescer até overfitting
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)

# Treinando
model.fit(X_train, y_train)

# ======================================================
# 6) Predição e avaliação
# ======================================================

y_pred = model.predict(X_test)

print("\nAcurácia:", accuracy_score(y_test, y_pred))
print("\nRelatório de classificação:\n")
print(classification_report(y_test, y_pred))

# Erros
df_resultados = pd.DataFrame({
    "real": y_test,
    "previsto": y_pred
}, index=X_test.index)

df_erros = df_resultados[df_resultados["real"] != df_resultados["previsto"]]

print("\nCasos em que o modelo errou:")
print(df_erros)