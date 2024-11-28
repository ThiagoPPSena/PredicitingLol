import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from dataLcu import getAllData
from model import loadModel
import time
import os

modelTree = loadModel("model.pkl")

# Prever ao vivo
numberTest = 300
for attempt in range(numberTest):
    # Limpar o terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    dataLive = getAllData()
    print(f"Teste {attempt + 1}/{numberTest}")
    print(dataLive.head())
    dataLiveArray = dataLive.to_numpy()
    predProbaLive = modelTree.predict_proba(dataLiveArray)
    probTeam1 = predProbaLive[0][0]  # Probabilidade do time 1 ganhar
    probTeam2 = predProbaLive[0][1]  # Probabilidade do time 2 ganhar
    print(f"Probabilidade do Time 1 ganhar: {probTeam1 * 100:.2f}%")
    print(f"Probabilidade do Time 2 ganhar: {probTeam2 * 100:.2f}%")
    time.sleep(3)