from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preProcessing():
    data = pd.read_csv('matches.csv')

    # Inicializando o MinMaxScaler
    scaler = MinMaxScaler()

    # Ajustando e transformando os dados
    dataNormalized = scaler.fit_transform(data)

    return dataNormalized

def optimizing():
    pass

def randomForest():
    pass


data = preProcessing()
# Separar as variáveis independentes (X) e a variável dependente (y)
# Excluindo a coluna 1 (segunda coluna, index 1)
X = np.delete(data, -1, axis=1)
y = data[:, -1]

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
model = RandomForestClassifier(n_estimators=40, random_state=42)
model.fit(X_train, y_train)

# Avaliar o modelo
y_pred = model.predict(X_test)
print(f"Acurácia: {accuracy_score(y_test, y_pred)}")
