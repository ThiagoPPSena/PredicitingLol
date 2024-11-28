import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Carregar o dataset
data = pd.read_csv("matches.csv")

# Verificar o balanceamento das classes

# Selecionar as features e o rótulo
X = data[
    [
        "totalGoldA",
        "totalGoldB",
        "destroyedTowersA",
        "destroyedTowersB",
        "destroyedNexusTowersA",
        "destroyedNexusTowersB",
        "destroyedInhibitorsA",
        "destroyedInhibitorsB",
        "dragonsA",
        "dragonsB",
        "baronsA",
        "baronsB",
    ]
]
y = data["winTeam"]
print(y.value_counts())

# Dividir os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar e treinar o modelo com balanceamento de classes
model = DecisionTreeClassifier(random_state=42, class_weight='balanced') ## add balanced
model.fit(X_train, y_train)

# Fazer previsões
y_pred = model.predict(X_test)

# Avaliar o modelo
print("Acurácia:", accuracy_score(y_test, y_pred))
print("\nRelatório de Classificação:\n", classification_report(y_test, y_pred))




# # Exibir a matriz de confusão
# ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, display_labels=["Team 2", "Team 1"])
# plt.show()

# # Visualizar a árvore de decisão (opcional)
# from sklearn.tree import plot_tree

# plt.figure(figsize=(20, 10))
# plot_tree(
#     model,
#     feature_names=X.columns,
#     class_names=["Team 2", "Team 1"],
#     filled=True,
#     fontsize=10,
# )
# plt.show()
