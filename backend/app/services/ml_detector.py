import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import List, Dict
from datetime import datetime

class MLDetector:
    """Détecteur de fraude basé sur Machine Learning"""
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'amount', 'hour', 'day_of_week', 
            'is_weekend', 'transaction_count_last_hour'
        ]
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.model = IsolationForest(
                contamination=0.1,  # 10% de fraudes attendues
                random_state=42,
                n_estimators=100
            )
    
    def prepare_features(self, transactions: List[Dict]) -> pd.DataFrame:
        """Prépare les features pour le ML"""
        df = pd.DataFrame(transactions)
        
        # Features temporelles
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Fréquence des transactions
        df = df.sort_values('timestamp')
        df['transaction_count_last_hour'] = 0
        
        for user_id in df['user_id'].unique():
            user_mask = df['user_id'] == user_id
            user_df = df[user_mask].copy()
            
            for idx in user_df.index:
                current_time = user_df.loc[idx, 'timestamp']
                time_window = pd.Timedelta(hours=1)
                recent = user_df[
                    (user_df['timestamp'] < current_time) &
                    (user_df['timestamp'] >= current_time - time_window)
                ]
                df.loc[idx, 'transaction_count_last_hour'] = len(recent)
        
        return df[self.feature_columns]
    
    def train(self, transactions: List[Dict]):
        """Entraîne le modèle sur les données"""
        X = self.prepare_features(transactions)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        
        return self.evaluate(transactions)
    
    def predict(self, transactions: List[Dict]) -> List[Dict]:
        """Prédit les fraudes pour de nouvelles transactions"""
        if self.model is None:
            raise ValueError("Le modèle n'est pas entraîné")
        
        X = self.prepare_features(transactions)
        X_scaled = self.scaler.transform(X)
        
        # Prédictions (-1 = anomalie/fraude, 1 = normal)
        predictions = self.model.predict(X_scaled)
        
        # Scores d'anomalie (plus négatif = plus suspect)
        scores = self.model.score_samples(X_scaled)
        
        # Normaliser les scores entre 0 et 1
        normalized_scores = self._normalize_scores(scores)
        
        results = []
        for i, trans in enumerate(transactions):
            is_fraud = predictions[i] == -1
            score = normalized_scores[i]
            
            results.append({
                'transaction_id': trans['transaction_id'],
                'score': float(score),
                'is_fraud': bool(is_fraud),
                'severity': self._get_severity(score),
                'reasons': [f"Score d'anomalie ML: {score:.3f}"] if is_fraud else []
            })
        
        return results
    
    def _normalize_scores(self, scores: np.ndarray) -> np.ndarray:
        """Normalise les scores entre 0 et 1"""
        min_score = scores.min()
        max_score = scores.max()
        
        if max_score - min_score == 0:
            return np.zeros_like(scores)
        
        normalized = (scores - min_score) / (max_score - min_score)
        # Inverser: score faible = plus suspect
        return 1 - normalized
    
    def _get_severity(self, score: float) -> str:
        """Détermine la sévérité selon le score"""
        if score >= 0.8:
            return "critical"
        elif score >= 0.6:
            return "high"
        elif score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def evaluate(self, transactions: List[Dict], labels: List[int] = None) -> Dict:
        """Évalue les performances du modèle"""
        if labels is None:
            # Si pas de labels, retourner métriques basiques
            predictions = self.predict(transactions)
            fraud_count = sum(1 for p in predictions if p['is_fraud'])
            
            return {
                'total_transactions': len(transactions),
                'frauds_detected': fraud_count,
                'fraud_rate': fraud_count / len(transactions) if transactions else 0
            }
        
        # Avec labels, calculer précision/rappel
        from sklearn.metrics import precision_score, recall_score, f1_score
        
        X = self.prepare_features(transactions)
        X_scaled = self.scaler.transform(X)
        predictions = (self.model.predict(X_scaled) == -1).astype(int)
        
        return {
            'precision': float(precision_score(labels, predictions)),
            'recall': float(recall_score(labels, predictions)),
            'f1_score': float(f1_score(labels, predictions)),
            'total_transactions': len(transactions)
        }
    
    def save_model(self, path: str):
        """Sauvegarde le modèle"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }, path)
    
    def load_model(self, path: str):
        """Charge un modèle sauvegardé"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_columns = data['feature_columns']
