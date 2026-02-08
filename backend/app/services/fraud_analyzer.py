from typing import List, Dict
import time
from app.services.rule_detector import RuleBasedDetector
from app.services.ml_detector import MLDetector

class FraudAnalyzer:
    """Service principal combinant règles et ML"""
    
    def __init__(self, ml_model_path: str = None):
        self.rule_detector = RuleBasedDetector()
        self.ml_detector = MLDetector(ml_model_path)
        
        # Poids pour le score combiné
        self.weights = {
            'rules': 0.4,
            'ml': 0.6
        }
    
    def analyze_transactions(
        self, 
        transactions: List[Dict],
        use_rules: bool = True,
        use_ml: bool = True
    ) -> Dict:
        """
        Analyse des transactions avec approche hybride
        
        Args:
            transactions: Liste des transactions
            use_rules: Utiliser la détection par règles
            use_ml: Utiliser la détection ML
        
        Returns:
            Dict avec résultats d'analyse
        """
        start_time = time.time()
        
        results = []
        rule_results = []
        ml_results = []
        
        # Détection par règles
        if use_rules:
            rule_results = self.rule_detector.batch_analyze(transactions)
        
        # Détection ML
        if use_ml and self.ml_detector.model is not None:
            try:
                ml_results = self.ml_detector.predict(transactions)
            except Exception as e:
                print(f"Erreur ML: {e}")
                ml_results = []
        
        # Combiner les résultats
        for i, trans in enumerate(transactions):
            combined_result = self._combine_results(
                trans,
                rule_results[i] if i < len(rule_results) else None,
                ml_results[i] if i < len(ml_results) else None,
                use_rules,
                use_ml
            )
            results.append(combined_result)
        
        # Statistiques
        frauds_detected = sum(1 for r in results if r['is_fraud'])
        avg_score = sum(r['score'] for r in results) / len(results) if results else 0
        
        processing_time = time.time() - start_time
        
        return {
            'results': results,
            'stats': {
                'total_analyzed': len(transactions),
                'frauds_detected': frauds_detected,
                'average_risk_score': avg_score,
                'processing_time': processing_time
            }
        }
    
    def _combine_results(
        self,
        transaction: Dict,
        rule_result: Dict,
        ml_result: Dict,
        use_rules: bool,
        use_ml: bool
    ) -> Dict:
        """Combine les résultats des deux méthodes"""
        
        # Initialiser
        combined_score = 0.0
        is_fraud = False
        reasons = []
        severity = "low"
        fraud_type = None
        
        # Combiner selon ce qui est activé
        if use_rules and rule_result:
            combined_score += rule_result['score'] * self.weights['rules']
            reasons.extend(rule_result['reasons'])
            is_fraud = is_fraud or rule_result['is_fraud']
            if rule_result['is_fraud']:
                fraud_type = "rule_based"
        
        if use_ml and ml_result:
            combined_score += ml_result['score'] * self.weights['ml']
            reasons.extend(ml_result['reasons'])
            is_fraud = is_fraud or ml_result['is_fraud']
            if ml_result['is_fraud']:
                fraud_type = "ml_based" if fraud_type is None else "hybrid"
        
        # Ajuster si un seul système utilisé
        if use_rules and not use_ml:
            combined_score = rule_result['score'] if rule_result else 0.0
        elif use_ml and not use_rules:
            combined_score = ml_result['score'] if ml_result else 0.0
        
        # Déterminer sévérité
        severity = self._get_severity(combined_score)
        
        return {
            'transaction_id': transaction['transaction_id'],
            'amount': transaction['amount'],
            'timestamp': transaction['timestamp'].isoformat() if hasattr(transaction['timestamp'], 'isoformat') else str(transaction['timestamp']),
            'merchant': transaction.get('merchant'),
            'user_id': transaction['user_id'],
            'score': round(combined_score, 3),
            'is_fraud': is_fraud,
            'fraud_type': fraud_type,
            'severity': severity,
            'reasons': reasons,
            'details': {
                'rule_score': rule_result['score'] if rule_result else None,
                'ml_score': ml_result['score'] if ml_result else None
            }
        }
    
    def _get_severity(self, score: float) -> str:
        """Détermine la sévérité selon le score combiné"""
        if score >= 0.75:
            return "critical"
        elif score >= 0.55:
            return "high"
        elif score >= 0.35:
            return "medium"
        else:
            return "low"
    
    def train_ml_model(self, transactions: List[Dict]) -> Dict:
        """Entraîne le modèle ML"""
        return self.ml_detector.train(transactions)
    
    def save_ml_model(self, path: str):
        """Sauvegarde le modèle ML"""
        self.ml_detector.save_model(path)
    
    def get_model_info(self) -> Dict:
        """Retourne les infos sur les modèles utilisés"""
        return {
            'rule_based': {
                'enabled': True,
                'rules_count': len(self.rule_detector.rules),
                'weight': self.weights['rules']
            },
            'ml_based': {
                'enabled': self.ml_detector.model is not None,
                'model_type': 'IsolationForest',
                'weight': self.weights['ml']
            }
        }
