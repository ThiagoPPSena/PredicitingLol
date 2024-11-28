from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def preProcessing():
    data = pd.read_csv('matches.csv')

    # Inicializando o MinMaxScaler
    scaler = MinMaxScaler()

    # Ajustando e transformando os dados
    dataNormalized = scaler.fit_transform(data)

    return dataNormalized

def validation(model, features, output):
    # Definir os parâmetros para o K-Fold Cross Validation
    kf = KFold(n_splits=10, shuffle=True, random_state=42)

    # Listas para armazenar os resultados da validação cruzada
    accuracyList = []
    precisionList = []
    recallList = []
    f1List = []

    # Realizar validação cruzada
    for trainIndex, valIndex in kf.split(features):
        featuresTrain, featuresVal = features[trainIndex], features[valIndex]
        outputTrain, outputVal = output[trainIndex], output[valIndex]
        
        # Treinar o modelo
        model.fit(featuresTrain, outputTrain)
        
        # Fazer previsões
        outputPred = model.predict(featuresVal)
        
        # Avaliar as métricas
        accuracy = accuracy_score(outputVal, outputPred)
        precision = precision_score(outputVal, outputPred, average='weighted', zero_division=0)
        recall = recall_score(outputVal, outputPred, average='weighted', zero_division=0)
        f1 = f1_score(outputVal, outputPred, average='weighted', zero_division=0)

        # Armazenar os resultados
        accuracyList.append(accuracy)
        precisionList.append(precision)
        recallList.append(recall)
        f1List.append(f1)

    # Calcular a média e desvio padrão de cada métrica
    accuracyMean = round(np.mean(accuracyList), 4)
    accuracyStd = round(np.std(accuracyList), 4)
    precisionMean = round(np.mean(precisionList), 4)
    recallMean = round(np.mean(recallList), 4)
    f1Mean = round(np.mean(f1List), 4)

    # Imprimir as métricas
    print("Média da Acurácia:", accuracyMean)
    print("Desvio Padrão da Acurácia:", accuracyStd)
    print("Média da Precisão:", precisionMean)
    print("Média do Recall:", recallMean)
    print("Média do F1-Score:", f1Mean)

def chooseParams(featuresTrain, outputTrain):
    # Ajuste de hiperparâmetros com GridSearchCV
    paramGrid = {
        'n_estimators': [100, 200, 300],       # Número de árvores
        'max_depth': [None, 10, 20],          # Profundidade máxima
        'min_samples_split': [2, 5],          # Mínimo de amostras para dividir
        'min_samples_leaf': [1, 2]            # Mínimo de amostras em uma folha
    }

    model = RandomForestClassifier(random_state=42)

    gridSearch = GridSearchCV(
        estimator=model,
        param_grid=paramGrid,
        cv=10,  # 10 folds para validação cruzada
        scoring='accuracy',
        verbose=2,
        n_jobs=-1
    )

    # Realizar o ajuste de hiperparâmetros
    print("Ajustando hiperparâmetros...")
    gridSearch.fit(featuresTrain, outputTrain)

    # Melhor combinação de hiperparâmetros
    bestParams = gridSearch.best_params_
    print("Melhores hiperparâmetros:", bestParams)

    # Treinar o modelo final com os melhores hiperparâmetros
    bestModel = gridSearch.best_estimator_
    return bestModel

def randomForest():
    data = preProcessing()

    # Separar as variáveis independentes (X) e a variável dependente (y)
    X = np.delete(data, -1, axis=1)
    y = data[:, -1]

    # Dividir os dados em treino (com validação) e teste
    featuresTrain, featuresTest, outputTrain, outputTest = train_test_split(X, y, test_size=0.3, random_state=42)

    bestModel = chooseParams(featuresTrain, outputTrain) 

    # Validar o modelo ajustado
    print("Validação cruzada com o melhor modelo:")
    validation(bestModel, featuresTrain, outputTrain)

    # Avaliar no conjunto de teste
    print("Avaliando no conjunto de teste...")
    outputPred = bestModel.predict(featuresTest)

    # Exibir a matriz de confusão no conjunto de teste
    cmTest = confusion_matrix(outputTest, outputPred)
    dispTest = ConfusionMatrixDisplay(confusion_matrix=cmTest)
    dispTest.plot(cmap=plt.cm.Blues)
    plt.title("Matriz de Confusão (Teste)")
    plt.show()

# Chamar a função principal
randomForest()