import sys
import os
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
import numpy as np
import joblib
from constant import Constant
from preprocessing import LogPreprocessor
sys.path.append(os.getcwd())

class AnomalyDetector:
    def __init__(self):
        self.isolation_forest = IsolationForest(
            n_jobs=-1,
            verbose=True,
            contamination=0.05
        )
        self.one_svm = OneClassSVM(
            verbose=True,
            nu=0.05
            )

    def train_models(self,X:np.ndarray):
        """
            Train isolation Forest and class SVM models
        """
        self.isolation_forest.fit(X)
        self.one_svm.fit(X)

        joblib.dump(self.isolation_forest,Constant.ISOLATION_FOREST_MODEL_FILE_NAME)
        joblib.dump(self.one_svm, Constant.ONE_CLASS_SVM_MODEL_FILE_NAME)

    def predict(self, X:np.ndarray)->dict[str,np.ndarray]:
        """
            Make prediction on X using isolation forest and one class svm models
        """
        isolation_forest: IsolationForest = joblib.load(Constant.ISOLATION_FOREST_MODEL_FILE_NAME)
        one_class_svm: OneClassSVM = joblib.load(Constant.ONE_CLASS_SVM_MODEL_FILE_NAME)

        return {
                "isolation_forest": isolation_forest.predict(X),
                "one_class_svm": one_class_svm.predict(X)
        }
    
    def compute_anomaly_score(self,X:np.ndarray)-> dict[str,np.ndarray]:
        """
            Compute anomaly score per model (isolation forest and one class svm)
        """
        isolation_forest: IsolationForest = joblib.load(Constant.ISOLATION_FOREST_MODEL_FILE_NAME)
        one_class_svm: OneClassSVM = joblib.load(Constant.ONE_CLASS_SVM_MODEL_FILE_NAME)

        return {
                "isolation_forest": isolation_forest.decision_function(X),
                "one_class_svm": one_class_svm.decision_function(X)
        }
    
    def evaluate_models(self,X:np.ndarray):
        """
            Evaluate Isolation Forest and One Class svm models
        """
        scores = self.compute_anomaly_score(X)

        fig,(ax1,ax2) = plt.subplots(2,1)

        ax1.hist(scores['isolation_forest'], bins=20, color='blue',alpha=.7)
        ax1.set_title("Histogramme isolation forest")

        ax2.hist(scores['one_class_svm'], bins=20, color='green',alpha=.7)
        ax2.set_title("Histogramme One class svm")

        plt.xlabel("Score d'anomalies")
        plt.ylabel("Fréquences")
        plt.tight_layout()
        plt.show()

        prediction = self.predict(X)
        outliers_isolation_forest_ration = np.mean(prediction['isolation_forest']==-1)
        outliers_one_class_svm_ration = np.mean(prediction['one_class_svm']==-1)


    
        print(f"Isolation Forest outliers ratio: {outliers_isolation_forest_ration:.2%}")
        print(f"One-Class SVM outliers ratio: {outliers_one_class_svm_ration:.2%}")


if __name__ == "__main__":
    df = pd.read_csv(Constant.LOGS_DATA_FILE_NAME)

    preprocessor = LogPreprocessor()
    df_train,df_test = preprocessor.split_dataset(df)

    print("Prétraitement des données...")

    x_train, df_train_engineered = preprocessor.fit_transform(df_train)
    x_test, df_test_engineered = preprocessor.fit_transform(df_test)

    detector = AnomalyDetector()

    if os.path.exists(Constant.ISOLATION_FOREST_MODEL_FILE_NAME) and os.path.exists(Constant.ONE_CLASS_SVM_MODEL_FILE_NAME):
        print("Evaluation des model de test set")
        detector.evaluate_models(x_test)
    else :
        print(" Entrainement modèle...")
        detector.train_models(x_train)

        print("Evaluation des model de test set")
        detector.evaluate_models(x_test)
    
    #Debogage
    #predictions = detector.predict(x_test)