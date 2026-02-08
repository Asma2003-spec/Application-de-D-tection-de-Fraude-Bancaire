import numpy as np
from datetime import datetime, time
from typing import Dict, List
import pandas as pd

class RuleBasedDetector:
    """Détecteur de fraude basé sur des règles métier"""
    
    def __init__(self):
        self.rules = {
            'high_amount': {'threshold': 1000, 'weight': 0.3},
            'unusual_time': {'weight': 0.2},
            'high_frequency': {'threshold': 5, 'weight': 0.25},
            'unusual_location': {'weight': 0.15},
            'amount_deviation': {'std_threshold': 3, 'weight': 0.1}
        }
    
    def analyze_transaction(self, transaction: Dict, user_history: List[Dict] = None) -> Dict:
        """
        Analyse une transaction selon les règles définies
        
        Returns:
            Dict avec score, is_fraud, reasons
        """
        scores = []
        reasons = []
        
        # Règle 1: Montant élevé
        if transaction['amount'] > self.rules['high_amount']['threshold']:
            scores.append(self.rules['high_amount']['weight'])
            reasons.append(f"Montant élevé: {transaction['amount']}€")
        
        # Règle 2: Heure inhabituelle (entre 23h et 6h)
        hour = transaction['timestamp'].hour
        if hour >= 23 or hour < 6:
            scores.append(self.rules['unusual_time']['weight'])
            reasons.append(f"Transaction à {hour}h (heure inhabituelle)")
        
        # Règle 3: Fréquence élevée (si historique disponible)
        if user_history:
            recent_count = self._count_recent_transactions(
                transaction['timestamp'], 
                user_history
            )
            if recent_count >= self.rules['high_frequency']['threshold']:
                scores.append(self.rules['high_frequency']['weight'])
                reasons.append(f"{recent_count} transactions dans la dernière heure")
        
        # Règle 4: Déviation du montant moyen
        if user_history:
            avg_amount = np.mean([t['amount'] for t in user_history])
            std_amount = np.std([t['amount'] for t in user_history])
            
            if std_amount > 0:
                z_score = abs((transaction['amount'] - avg_amount) / std_amount)
                if z_score > self.rules['amount_deviation']['std_threshold']:
                    scores.append(self.rules['amount_deviation']['weight'])
                    reasons.append(f"Montant anormal (z-score: {z_score:.2f})")
        
        # Calcul du score final
        final_score = sum(scores) if scores else 0.0
        is_fraud = final_score >= 0.5
        
        return {
            'score': min(final_score, 1.0),
            'is_fraud': is_fraud,
            'reasons': reasons,
            'severity': self._get_severity(final_score)
        }
    
    def _count_recent_transactions(self, current_time: datetime, history: List[Dict]) -> int:
        """Compte les transactions dans la dernière heure"""
        count = 0
        for trans in history:
            time_diff = (current_time - trans['timestamp']).total_seconds() / 3600
            if 0 < time_diff <= 1:
                count += 1
        return count
    
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
    
    def batch_analyze(self, transactions: List[Dict]) -> List[Dict]:
        """Analyse un lot de transactions"""
        results = []
        
        # Grouper par user_id pour l'historique
        df = pd.DataFrame(transactions)
        
        for idx, trans in enumerate(transactions):
            user_history = df[
                (df['user_id'] == trans['user_id']) & 
                (df.index < idx)
            ].to_dict('records')
            
            result = self.analyze_transaction(trans, user_history)
            result['transaction_id'] = trans['transaction_id']
            results.append(result)
        
        return results
