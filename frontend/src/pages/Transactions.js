import React, { useState, useEffect } from 'react';
import { getTransactions } from '../services/api';
import './Transactions.css';

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    user_id: '',
    is_fraud: null
  });
  const [page, setPage] = useState(0);
  const limit = 50;

  useEffect(() => {
    loadTransactions();
  }, [page, filters]);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const params = {
        skip: page * limit,
        limit: limit,
        ...(filters.user_id && { user_id: filters.user_id }),
        ...(filters.is_fraud !== null && { is_fraud: filters.is_fraud })
      };
      
      const response = await getTransactions(params);
      setTransactions(response.data);
    } catch (error) {
      console.error('Erreur chargement transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setPage(0);
  };

  const getRiskBadge = (score) => {
    if (score >= 0.75) return <span className="badge badge-critical">Critique</span>;
    if (score >= 0.55) return <span className="badge badge-high">Élevé</span>;
    if (score >= 0.35) return <span className="badge badge-medium">Moyen</span>;
    return <span className="badge badge-low">Faible</span>;
  };

  return (
    <div className="transactions">
      <h2>💳 Transactions</h2>

      {/* Filtres */}
      <div className="filters">
        <div className="filter-group">
          <label>User ID:</label>
          <input 
            type="text" 
            placeholder="USER_001"
            value={filters.user_id}
            onChange={(e) => handleFilterChange('user_id', e.target.value)}
          />
        </div>

        <div className="filter-group">
          <label>Statut:</label>
          <select 
            value={filters.is_fraud === null ? '' : filters.is_fraud}
            onChange={(e) => handleFilterChange('is_fraud', e.target.value === '' ? null : e.target.value === 'true')}
          >
            <option value="">Toutes</option>
            <option value="true">Fraudes uniquement</option>
            <option value="false">Normales uniquement</option>
          </select>
        </div>

        <button onClick={() => {
          setFilters({ user_id: '', is_fraud: null });
          setPage(0);
        }} className="btn-secondary">
          🔄 Réinitialiser
        </button>
      </div>

      {/* Table */}
      {loading ? (
        <div className="loading">Chargement...</div>
      ) : (
        <>
          <div className="table-container">
            <table className="transactions-table">
              <thead>
                <tr>
                  <th>ID Transaction</th>
                  <th>User ID</th>
                  <th>Montant</th>
                  <th>Merchant</th>
                  <th>Date</th>
                  <th>Score Risque</th>
                  <th>Statut</th>
                  <th>Type Fraude</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map(trans => (
                  <tr key={trans.id} className={trans.is_fraud ? 'fraud-row' : ''}>
                    <td className="mono">{trans.transaction_id}</td>
                    <td>{trans.user_id}</td>
                    <td className="amount">{trans.amount.toFixed(2)}€</td>
                    <td>{trans.merchant || '-'}</td>
                    <td>{new Date(trans.timestamp).toLocaleString('fr-FR')}</td>
                    <td>
                      <div className="risk-score">
                        <span className="score-value">{trans.risk_score.toFixed(3)}</span>
                        {getRiskBadge(trans.risk_score)}
                      </div>
                    </td>
                    <td>
                      {trans.is_fraud ? 
                        <span className="badge badge-danger">🚨 Fraude</span> : 
                        <span className="badge badge-success">✅ Normal</span>
                      }
                    </td>
                    <td>{trans.fraud_type || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="pagination">
            <button 
              onClick={() => setPage(p => Math.max(0, p - 1))}
              disabled={page === 0}
              className="btn-secondary"
            >
              ← Précédent
            </button>
            
            <span className="page-info">Page {page + 1}</span>
            
            <button 
              onClick={() => setPage(p => p + 1)}
              disabled={transactions.length < limit}
              className="btn-secondary"
            >
              Suivant →
            </button>
          </div>

          <div className="summary">
            <p>Affichage de {transactions.length} transactions</p>
          </div>
        </>
      )}
    </div>
  );
}

export default Transactions;
