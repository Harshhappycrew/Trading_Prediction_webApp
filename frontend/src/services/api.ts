/**
 * API Service for QuantEdge Backend
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  // Health
  health: () => fetch(`${API_BASE_URL}/api/health`).then(r => r.json()),
  
  // Portfolio
  getPositions: () => fetch(`${API_BASE_URL}/api/portfolio/positions`).then(r => r.json()),
  getMetrics: () => fetch(`${API_BASE_URL}/api/portfolio/metrics`).then(r => r.json()),
  getPerformance: (days = 30) => fetch(`${API_BASE_URL}/api/portfolio/performance?days=${days}`).then(r => r.json()),
  
  // Trading
  getTrades: (limit = 50) => fetch(`${API_BASE_URL}/api/trading/trades?limit=${limit}`).then(r => r.json()),
  createOrder: (order: any) => fetch(`${API_BASE_URL}/api/trading/orders`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(order)
  }).then(r => r.json()),
  
  // ML
  getSignals: () => fetch(`${API_BASE_URL}/api/ml/signals`).then(r => r.json()),
  getPredictions: (symbol: string) => fetch(`${API_BASE_URL}/api/ml/predictions/${symbol}`).then(r => r.json()),
  
  // Data
  getPrice: (symbol: string, days = 30) => fetch(`${API_BASE_URL}/api/data/price/${symbol}?days=${days}`).then(r => r.json()),
};
