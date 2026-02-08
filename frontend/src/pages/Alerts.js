import React, { useState, useEffect } from 'react';
import { getAlerts, updateAlert } from '../services/api';
import './Alerts.css';

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [statusFilter, setStatusFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');

  useEffect(() => {
    loadAlerts();
  }, [statusFilter, severityFilter]);

  const loadAlerts = async () => {
    try {
      setLoading(true);
      const params = {};
      if (statusFilter) params.status = statusFilter;
      if (severityFilter) params.severity = severityFilter;
      
      const response = await getAlerts(params);
      setAlerts(response.data);
    } catch (error) {
      console.error('Erreur chargement alertes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (alertId, newStatus) => {
    try {
      await updateAlert(alertId, {
        status: newStatus,
        reviewed_by: 'Admin'
      });
      
      // Recharger les alertes
      loadAlerts();
      alert(`✅ Alerte ${newStatus === 'confirmed' ? 'confirmée' : 'rejetée'}`);
    } catch (error) {
      console.error('Erreur mise à jour:', error);
      alert('❌ Erreur lors de la mise à jour');
    }
  };

  const getSeverityBadge = (severity) => {
    const badges = {
      critical: <span className="badge badge-critical">🔴 Critique</span>,
      high: <span className="badge badge-high">🟠 Élevé</span>,
      medium: <span className="badge badge-medium">🟡 Moyen</span>,
      low: <span className="badge badge-low">🟢 Faible</span>
    };
    return badges[severity] || severity;
  };

  const getStatusBadge = (status) => {
    const badges = {
      pending: <span className="badge badge-warning">⏳ En attente</span>,
      confirmed: <span className="badge badge-danger">✅ Confirmée</span>,
      rejected: <span className="badge badge-success">❌ Rejetée</span>
    };
    return badges[status] || status;
  };

  return (
    <div className="alerts">
      <h2>🚨 Alertes de Fraude</h2>

      {/* Filtres */}
      <div className="filters">
        <div className="filter-group">
          <label>Statut:</label>
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="">Tous</option>
            <option value="pending">En attente</option>
            <option value="confirmed">Confirmées</option>
            <option value="rejected">Rejetées</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Sévérité:</label>
          <select value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}>
            <option value="">Toutes</option>
            <option value="critical">Critique</option>
            <option value="high">Élevé</option>
            <option value="medium">Moyen</option>
            <option value="low">Faible</option>
          </select>
        </div>

        <button onClick={loadAlerts} className="btn-primary">
          🔄 Rafraîchir
        </button>
      </div>

      {/* Liste des alertes */}
      {loading ? (
        <div className="loading">Chargement...</div>
      ) : (
        <div className="alerts-grid">
          {alerts.length === 0 ? (
            <div className="no-data">
              <p>Aucune alerte trouvée</p>
            </div>
          ) : (
            alerts.map(alert => (
              <div key={alert.id} className={`alert-card ${alert.severity}`}>
                <div className="alert-header">
                  <div className="alert-id">
                    <strong>Alerte #{alert.id}</strong>
                    {getSeverityBadge(alert.severity)}
                  </div>
                  {getStatusBadge(alert.status)}
                </div>

                <div className="alert-body">
                  <div className="alert-info">
                    <p><strong>Transaction:</strong> {alert.transaction_id}</p>
                    <p><strong>Type:</strong> {alert.alert_type}</p>
                    <p><strong>Score:</strong> <span className="score">{alert.risk_score.toFixed(3)}</span></p>
                  </div>

                  <div className="alert-reason">
                    <strong>Raisons:</strong>
                    <p>{alert.reason}</p>
                  </div>

                  <div className="alert-meta">
                    <small>Créée le: {new Date(alert.created_at).toLocaleString('fr-FR')}</small>
                    {alert.reviewed_at && (
                      <small>Traitée le: {new Date(alert.reviewed_at).toLocaleString('fr-FR')} par {alert.reviewed_by}</small>
                    )}
                  </div>
                </div>

                {alert.status === 'pending' && (
                  <div className="alert-actions">
                    <button 
                      onClick={() => handleStatusUpdate(alert.id, 'confirmed')}
                      className="btn-danger"
                    >
                      ✅ Confirmer Fraude
                    </button>
                    <button 
                      onClick={() => handleStatusUpdate(alert.id, 'rejected')}
                      className="btn-success"
                    >
                      ❌ Rejeter
                    </button>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}

      <div className="summary">
        <p>{alerts.length} alerte(s) affichée(s)</p>
      </div>
    </div>
  );
}

export default Alerts;
