import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getStats, getDailyStats, getStatsBySeverity } from '../services/api';
import './Dashboard.css';

const COLORS = ['#ff4444', '#ff9800', '#ffeb3b', '#4caf50'];

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [dailyStats, setDailyStats] = useState([]);
  const [severityStats, setSeverityStats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Charger les stats globales
      const statsResponse = await getStats();
      setStats(statsResponse.data);

      // Charger les stats quotidiennes
      const dailyResponse = await getDailyStats(30);
      
      // Combiner transactions et fraudes par jour
      const combinedDaily = dailyResponse.data.transactions.map(trans => {
        const fraud = dailyResponse.data.frauds.find(f => f.date === trans.date);
        return {
          date: trans.date,
          transactions: trans.count,
          frauds: fraud ? fraud.count : 0
        };
      });
      
      setDailyStats(combinedDaily);

      // Charger les stats par sévérité
      const severityResponse = await getStatsBySeverity();
      setSeverityStats(severityResponse.data);

    } catch (error) {
      console.error('Erreur lors du chargement:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Chargement...</div>;
  }

  return (
    <div className="dashboard">
      <h2>📊 Tableau de Bord</h2>

      {/* KPIs */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-icon">📈</div>
          <div className="kpi-content">
            <h3>Total Transactions</h3>
            <p className="kpi-value">{stats?.total_transactions || 0}</p>
          </div>
        </div>

        <div className="kpi-card danger">
          <div className="kpi-icon">⚠️</div>
          <div className="kpi-content">
            <h3>Fraudes Détectées</h3>
            <p className="kpi-value">{stats?.total_frauds || 0}</p>
          </div>
        </div>

        <div className="kpi-card warning">
          <div className="kpi-icon">📊</div>
          <div className="kpi-content">
            <h3>Taux de Fraude</h3>
            <p className="kpi-value">{stats?.fraud_rate || 0}%</p>
          </div>
        </div>

        <div className="kpi-card info">
          <div className="kpi-icon">💰</div>
          <div className="kpi-content">
            <h3>Montant à Risque</h3>
            <p className="kpi-value">{stats?.total_amount_at_risk?.toLocaleString() || 0}€</p>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon">🔔</div>
          <div className="kpi-content">
            <h3>Alertes Actives</h3>
            <p className="kpi-value">{stats?.pending_alerts || 0}</p>
          </div>
        </div>

        <div className="kpi-card success">
          <div className="kpi-icon">✅</div>
          <div className="kpi-content">
            <h3>Fraudes Confirmées</h3>
            <p className="kpi-value">{stats?.confirmed_frauds || 0}</p>
          </div>
        </div>
      </div>

      {/* Graphiques */}
      <div className="charts-grid">
        {/* Évolution temporelle */}
        <div className="chart-card">
          <h3>📈 Évolution des Transactions (30 jours)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={dailyStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => new Date(value).toLocaleDateString('fr-FR', { month: 'short', day: 'numeric' })}
              />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="transactions" stroke="#2196F3" name="Transactions" strokeWidth={2} />
              <Line type="monotone" dataKey="frauds" stroke="#f44336" name="Fraudes" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Alertes par sévérité */}
        <div className="chart-card">
          <h3>⚠️ Alertes par Sévérité</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={severityStats}
                dataKey="count"
                nameKey="severity"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(entry) => `${entry.severity}: ${entry.count}`}
              >
                {severityStats.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Bouton de rafraîchissement */}
      <div className="actions">
        <button onClick={loadData} className="btn-primary">
          🔄 Rafraîchir
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
