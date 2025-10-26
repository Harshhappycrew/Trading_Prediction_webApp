# QuantEdge: AI-Powered Trading Simulator

A production-ready, full-stack AI-powered quantitative trading simulator that predicts stock price movements using machine learning and executes simulated trades in real-time.

## 🚀 Features

- **Machine Learning Predictions**: LSTM neural network for price forecasting
- **Reinforcement Learning**: DQN/PPO agent for optimal trading decisions
- **Real-time Dashboard**: Modern React interface with live charts and analytics
- **Risk Management**: Position sizing, stop-loss, and portfolio optimization
- **Local-First**: Runs entirely on your laptop with SQLite database
- **Backtesting Engine**: Historical simulation with realistic costs
- **Technical Analysis**: RSI, MACD, Bollinger Bands, and more

## 📋 Requirements

- Docker & Docker Compose (recommended)
- **OR** Manual setup:
  - Python 3.9+
  - Node.js 18+
  - npm or yarn

## 🏃 Quick Start (Docker - Recommended)

### One-Command Setup

```bash
chmod +x setup.sh
./setup.sh
```

This will:
1. Create necessary directories
2. Set up environment configuration
3. Build Docker containers
4. Start all services

### Access the Application

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Managing Services

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build
```

## 💻 Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate 
#On Mac/Linux source venv/bin/activate  

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p data/raw data/processed data/models logs

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite+aiosqlite:///./data/quantedge.db
VITE_API_URL=http://localhost:8000
INITIAL_CAPITAL=1000000
CURRENCY=INR
CURRENCY_SYMBOL=₹
STOCK_EXCHANGE=NSE
```

## 📁 Project Structure

```
quantedge/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── api/                 # REST API endpoints
│   │   │   ├── health.py
│   │   │   ├── trading.py
│   │   │   ├── portfolio.py
│   │   │   ├── ml.py
│   │   │   └── data.py
│   │   ├── models/              # Database models
│   │   │   ├── stock_data.py
│   │   │   ├── trades.py
│   │   │   └── portfolio.py
│   │   ├── ml/                  # Machine learning
│   │   │   ├── lstm_predictor.py
│   │   │   └── rl_agent.py
│   │   ├── trading/             # Trading engine
│   │   │   └── engine.py
│   │   ├── data/                # Data collection
│   │   │   └── collector.py
│   │   └── database/            # Database setup
│   │       └── init_db.py
│   ├── data/                    # Local data storage
│   │   ├── raw/                 # Downloaded stock data
│   │   ├── processed/           # Processed features
│   │   └── models/              # Trained ML models
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                    # React TypeScript SPA
│   ├── src/
│   │   ├── components/
│   │   │   └── dashboard/       # Dashboard components
│   │   ├── pages/
│   │   ├── services/            # API integration
│   │   └── types/               # TypeScript types
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── setup.sh
└── README.md
```

## 🔧 API Endpoints

### Health & Status
- `GET /api/health` - Health check
- `GET /api/status` - System status

### Trading
- `POST /api/trading/orders` - Create trading order
- `GET /api/trading/trades` - Get trade history
- `GET /api/trading/orders` - Get order history

### Portfolio
- `GET /api/portfolio/positions` - Current positions
- `GET /api/portfolio/performance` - Performance history
- `GET /api/portfolio/metrics` - Portfolio metrics

### Machine Learning
- `GET /api/ml/predictions/{symbol}` - Get predictions
- `GET /api/ml/signals` - Current trading signals
- `POST /api/ml/train/{model_type}` - Train ML model

### Data
- `GET /api/data/price/{symbol}` - Historical prices
- `POST /api/data/sync/{symbol}` - Sync stock data
- `GET /api/data/symbols` - Available symbols

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📊 Machine Learning Models

### LSTM Price Predictor
- **Input**: 15-day window of OHLCV + technical indicators
- **Output**: Next-day price prediction with confidence
- **Architecture**: Stacked LSTM with dropout layers

### RL Trading Agent
- **Algorithm**: PPO (Proximal Policy Optimization)
- **Actions**: BUY, SELL, HOLD
- **Reward**: Risk-adjusted portfolio returns

## 📈 Performance Metrics

The dashboard displays:
- Total P&L and percentage returns
- Sharpe Ratio (risk-adjusted returns)
- Sortino Ratio (downside risk)
- Maximum Drawdown
- Win Rate
- Active positions count

## 🔒 Risk Management

- Position sizing based on portfolio value
- Stop-loss and take-profit levels
- Maximum drawdown limits
- Commission and slippage simulation (0.1%)

## 🛠️ Development

### Adding New Symbols

Edit `backend/app/data/collector.py`:

```python
self.symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "YOUR_SYMBOL"]
```

### Training ML Models

```bash
# Access backend container
docker-compose exec backend python

# Run training script
from app.data.collector import DataCollector
from app.ml.lstm_predictor import LSTMPredictor

# Fetch data
collector = DataCollector()
data = collector.fetch_all_symbols()

# Train LSTM
predictor = LSTMPredictor()
# ... training code
```

## 📝 License

This project is for educational and portfolio purposes.

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

## 📧 Contact

For questions or collaboration, please reach out via GitHub.

---

**Note**: This is a simulation tool for educational purposes. Do not use for actual trading without proper risk assessment and testing.
