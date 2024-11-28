import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from test import getAllData
import time

# Carregar o dataset
data = pd.read_csv("matches.csv")

# Selecionar as features e o rótulo
X = data[
    [
        "totalGoldA",
        "totalGoldB",
        "destroyedTowersA",
        "destroyedTowersB",
        "destroyedInhibitorsA",
        "destroyedInhibitorsB",
        "dragonsA",
        "dragonsB",
        "baronsA",
        "baronsB",
    ]
]
y = data["winTeam"]

# Dividir os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar e treinar o modelo com balanceamento de classes
model = RandomForestClassifier(random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Fazer previsões
y_pred = model.predict(X_test)

# Avaliar o modelo
print("Acurácia:", accuracy_score(y_test, y_pred))
print("\nRelatório de Classificação:\n", classification_report(y_test, y_pred))

# Prever ao vivo
numberTest = 60
for _ in range(numberTest):
    dataLive = getAllData()
    print(dataLive.head())
    predProbaLive = model.predict_proba(dataLive)
    probTeam1 = predProbaLive[0][1]  # Probabilidade do time 1 ganhar
    probTeam2 = predProbaLive[0][0]  # Probabilidade do time 2 ganhar
    print(f"Probabilidade do Time 1 ganhar: {probTeam1 * 100:.2f}%")
    print(f"Probabilidade do Time 2 ganhar: {probTeam2 * 100:.2f}%")
    predLive = model.predict(dataLive)
    print(predLive)
    print("Previsão ao vivo:", "Team 2" if predLive == 0 else "Team 1")
    time.sleep(10)