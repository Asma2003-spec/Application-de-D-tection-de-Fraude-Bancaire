"""
Générateur de données de transactions avec fraudes synthétiques
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_synthetic_transactions(num_transactions=1000, fraud_rate=0.05):
    """
    Génère des transactions synthétiques avec fraudes
    
    Args:
        num_transactions: Nombre total de transactions
        fraud_rate: Pourcentage de fraudes (0.05 = 5%)
    """
    
    np.random.seed(42)
    random.seed(42)
    
    # Configuration
    num_users = 50
    merchants = [
        'Amazon', 'Walmart', 'Target', 'BestBuy', 'Starbucks',
        'McDonalds', 'Shell Gas', 'Uber', 'Netflix', 'Spotify',
        'Apple Store', 'Google Play', 'Steam', 'PayPal', 'Airbnb',
        'Hotels.com', 'Delta Airlines', 'Hertz', 'Whole Foods', 'CVS'
    ]
    
    categories = [
        'Shopping', 'Food', 'Transport', 'Entertainment', 'Utilities',
        'Travel', 'Healthcare', 'Subscription', 'Fuel', 'Other'
    ]
    
    locations = [
        'Paris, FR', 'Lyon, FR', 'Marseille, FR', 'New York, US',
        'London, UK', 'Berlin, DE', 'Madrid, ES', 'Rome, IT',
        'Brussels, BE', 'Amsterdam, NL'
    ]
    
    transactions = []
    start_date = datetime.now() - timedelta(days=90)
    
    # Générer les transactions
    for i in range(num_transactions):
        # Utilisateur
        user_id = f"USER_{random.randint(1, num_users):03d}"
        
        # Timestamp (plus de transactions en journée)
        days_offset = random.randint(0, 90)
        hour_probs = [
            0.01, 0.01, 0.01, 0.01, 0.01, 0.02,  # 0-5h (nuit)
            0.03, 0.05, 0.07, 0.08, 0.07, 0.06,  # 6-11h (matin)
            0.06, 0.05, 0.05, 0.05, 0.06, 0.07,  # 12-17h (après-midi)
            0.08, 0.07, 0.05, 0.03, 0.02, 0.01   # 18-23h (soir)
        ]
        # Normaliser pour que la somme soit exactement 1
        hour_probs = np.array(hour_probs) / sum(hour_probs)
        hour = np.random.choice(range(24), p=hour_probs)
        
        timestamp = start_date + timedelta(days=days_offset, hours=int(hour), 
                                          minutes=random.randint(0, 59))
        
        # Montant (distribution log-normale)
        amount = np.random.lognormal(mean=3.5, sigma=1.2)
        amount = round(amount, 2)
        
        # Merchant et catégorie
        merchant = random.choice(merchants)
        category = random.choice(categories)
        location = random.choice(locations)
        
        transaction = {
            'transaction_id': f'TXN_{i+1:06d}',
            'user_id': user_id,
            'amount': amount,
            'timestamp': timestamp,
            'merchant': merchant,
            'category': category,
            'location': location
        }
        
        transactions.append(transaction)
    
    # Convertir en DataFrame
    df = pd.DataFrame(transactions)
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Injecter des fraudes
    num_frauds = int(num_transactions * fraud_rate)
    fraud_indices = np.random.choice(df.index, num_frauds, replace=False)
    
    for idx in fraud_indices:
        fraud_type = random.choice([
            'high_amount', 'unusual_time', 'high_frequency', 
            'unusual_location', 'multiple_types'
        ])
        
        if fraud_type == 'high_amount':
            # Montant anormalement élevé
            df.loc[idx, 'amount'] = random.uniform(2000, 5000)
        
        elif fraud_type == 'unusual_time':
            # Transaction en pleine nuit
            night_hour = random.choice([0, 1, 2, 3, 4, 5])
            original_time = df.loc[idx, 'timestamp']
            df.loc[idx, 'timestamp'] = original_time.replace(hour=night_hour)
        
        elif fraud_type == 'high_frequency':
            # Créer plusieurs transactions rapprochées
            user_id = df.loc[idx, 'user_id']
            base_time = df.loc[idx, 'timestamp']
            
            for j in range(3):
                new_trans = df.loc[idx].copy()
                new_trans['transaction_id'] = f'TXN_FRAUD_{idx}_{j}'
                new_trans['timestamp'] = base_time + timedelta(minutes=j*5)
                new_trans['amount'] = random.uniform(100, 500)
                df = pd.concat([df, pd.DataFrame([new_trans])], ignore_index=True)
        
        elif fraud_type == 'unusual_location':
            # Localisation étrangère inhabituelle
            df.loc[idx, 'location'] = 'Lagos, NG'
        
        elif fraud_type == 'multiple_types':
            # Combiner plusieurs indicateurs
            df.loc[idx, 'amount'] = random.uniform(1500, 3000)
            df.loc[idx, 'location'] = random.choice(['Moscow, RU', 'Beijing, CN'])
            night_hour = random.choice([1, 2, 3, 4])
            original_time = df.loc[idx, 'timestamp']
            df.loc[idx, 'timestamp'] = original_time.replace(hour=night_hour)
    
    # Trier par timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Reformater timestamp
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    return df


def main():
    """Génère et sauvegarde les données"""
    
    print("🔄 Génération des données...")
    
    # Générer différents datasets
    datasets = {
        'small': (500, 0.05),    # 500 transactions, 5% fraudes
        'medium': (2000, 0.08),  # 2000 transactions, 8% fraudes
        'large': (5000, 0.10)    # 5000 transactions, 10% fraudes
    }
    
    for name, (num_trans, fraud_rate) in datasets.items():
        df = generate_synthetic_transactions(num_trans, fraud_rate)
        
        filename = f'data/raw/transactions_{name}.csv'
        df.to_csv(filename, index=False)
        
        print(f"✅ Dataset '{name}' créé: {filename}")
        print(f"   - {len(df)} transactions")
        print(f"   - Période: {df['timestamp'].min()} à {df['timestamp'].max()}")
        print(f"   - Montant moyen: {df['amount'].mean():.2f}€")
        print(f"   - Taux de fraude cible: {fraud_rate*100}%\n")
    
    print("✨ Génération terminée!")


if __name__ == '__main__':
    main()
