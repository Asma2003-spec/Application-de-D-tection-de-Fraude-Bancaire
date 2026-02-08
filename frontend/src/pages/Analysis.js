import React, { useState } from 'react';
import { uploadCSV, analyzeTransactions, trainModel, getModelInfo } from '../services/api';
import './Analysis.css';

function Analysis() {
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [useRules, setUseRules] = useState(true);
  const [useMl, setUseMl] = useState(true);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadResult(null);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Veuillez sélectionner un fichier');
      return;
    }

    try {
      setLoading(true);
      const response = await uploadCSV(file);
      setUploadResult(response.data);
      alert('✅ Fichier importé avec succès!');
    } catch (error) {
      console.error('Erreur upload:', error);
      alert('❌ Erreur lors de l\'upload: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    try {
      setLoading(true);
      const response = await analyzeTransactions({
        use_rules: useRules,
        use_ml: useMl
      });
      setAnalysisResult(response.data);
      alert(`✅ Analyse terminée! ${response.data.frauds_detected} fraudes détectées`);
    } catch (error) {
      console.error('Erreur analyse:', error);
      alert('❌ Erreur lors de l\'analyse: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleTrain = async () => {
    if (!window.confirm('Entraîner le modèle ML? Cela peut prendre quelques minutes.')) {
      return;
    }

    try {
      setLoading(true);
      const response = await trainModel(100);
      alert(`✅ Modèle entraîné avec succès!\n${JSON.stringify(response.data.metrics, null, 2)}`);
      loadModelInfo();
    } catch (error) {
      console.error('Erreur training:', error);
      alert('❌ Erreur lors de l\'entraînement: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const loadModelInfo = async () => {
    try {
      const response = await getModelInfo();
      setModelInfo(response.data);
    } catch (error) {
      console.error('Erreur chargement model info:', error);
    }
  };

  React.useEffect(() => {
    loadModelInfo();
  }, []);

  return (
    <div className="analysis">
      <h2>🔍 Analyse de Fraude</h2>

      {/* Section Upload */}
      <div className="section">
        <h3>📤 Import de Données</h3>
        <div className="upload-area">
          <input 
            type="file" 
            accept=".csv" 
            onChange={handleFileChange}
            id="file-upload"
          />
          <label htmlFor="file-upload" className="file-label">
            {file ? `📄 ${file.name}` : '📁 Choisir un fichier CSV'}
          </label>
          
          <button 
            onClick={handleUpload} 
            disabled={!file || loading}
            className="btn-primary"
          >
            {loading ? '⏳ Upload...' : '⬆️ Importer'}
          </button>
        </div>

        {uploadResult && (
          <div className="result-box success">
            <h4>✅ Résultat de l'import</h4>
            <p>Transactions créées: <strong>{uploadResult.transactions_created}</strong></p>
            <p>Transactions ignorées (doublons): <strong>{uploadResult.transactions_skipped}</strong></p>
            <p>Total lignes: <strong>{uploadResult.total_rows}</strong></p>
          </div>
        )}
      </div>

      {/* Section Configuration */}
      <div className="section">
        <h3>⚙️ Configuration de l'Analyse</h3>
        <div className="config-options">
          <label className="checkbox-label">
            <input 
              type="checkbox" 
              checked={useRules} 
              onChange={(e) => setUseRules(e.target.checked)}
            />
            <span>Utiliser la détection par règles</span>
          </label>
          
          <label className="checkbox-label">
            <input 
              type="checkbox" 
              checked={useMl} 
              onChange={(e) => setUseMl(e.target.checked)}
            />
            <span>Utiliser le Machine Learning</span>
          </label>
        </div>

        <button 
          onClick={handleAnalyze} 
          disabled={loading || (!useRules && !useMl)}
          className="btn-primary btn-large"
        >
          {loading ? '⏳ Analyse en cours...' : '🚀 Lancer l\'Analyse'}
        </button>

        {analysisResult && (
          <div className="result-box info">
            <h4>📊 Résultats de l'Analyse</h4>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">Transactions analysées:</span>
                <span className="stat-value">{analysisResult.total_analyzed}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Fraudes détectées:</span>
                <span className="stat-value danger">{analysisResult.frauds_detected}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Score moyen:</span>
                <span className="stat-value">{analysisResult.average_risk_score.toFixed(3)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Alertes créées:</span>
                <span className="stat-value warning">{analysisResult.alerts_created}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Temps de traitement:</span>
                <span className="stat-value">{analysisResult.processing_time.toFixed(2)}s</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Section ML */}
      <div className="section">
        <h3>🤖 Machine Learning</h3>
        
        {modelInfo && (
          <div className="model-info">
            <div className="info-card">
              <h4>Détection par Règles</h4>
              <p>Status: <span className="badge success">Activé</span></p>
              <p>Nombre de règles: {modelInfo.rule_based.rules_count}</p>
              <p>Poids: {modelInfo.rule_based.weight * 100}%</p>
            </div>
            
            <div className="info-card">
              <h4>Détection ML</h4>
              <p>Status: 
                <span className={`badge ${modelInfo.ml_based.enabled ? 'success' : 'danger'}`}>
                  {modelInfo.ml_based.enabled ? 'Entraîné' : 'Non entraîné'}
                </span>
              </p>
              <p>Type: {modelInfo.ml_based.model_type}</p>
              <p>Poids: {modelInfo.ml_based.weight * 100}%</p>
            </div>
          </div>
        )}

        <button 
          onClick={handleTrain} 
          disabled={loading}
          className="btn-secondary"
        >
          {loading ? '⏳ Entraînement...' : '🎓 Entraîner le Modèle ML'}
        </button>
        
        <p className="help-text">
          ℹ️ L'entraînement nécessite au moins 100 transactions dans la base de données.
          Le modèle sera sauvegardé et utilisé automatiquement pour les prochaines analyses.
        </p>
      </div>
    </div>
  );
}

export default Analysis;
