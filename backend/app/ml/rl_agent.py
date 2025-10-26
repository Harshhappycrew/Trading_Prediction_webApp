"""
Reinforcement Learning Trading Agent
"""
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from gymnasium import Env, spaces
from loguru import logger
from pathlib import Path

class TradingEnvironment(Env):
    """Custom trading environment for RL agent"""
    
    def __init__(self, data, initial_balance=100000):
        super(TradingEnvironment, self).__init__()
        
        self.data = data
        self.initial_balance = initial_balance
        self.current_step = 0
        
        # State: [balance, shares_held, current_price, technical_indicators...]
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(15,), dtype=np.float32
        )
        
        # Actions: 0=HOLD, 1=BUY, 2=SELL
        self.action_space = spaces.Discrete(3)
        
        self.reset()
    
    def reset(self, seed=None, options=None):
        """Reset environment to initial state"""
        super().reset(seed=seed)
        self.current_step = 0
        self.balance = self.initial_balance
        self.shares_held = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0
        
        return self._get_observation(), {}
    
    def _get_observation(self):
        """Get current state observation"""
        if self.current_step >= len(self.data):
            self.current_step = len(self.data) - 1
        
        current_price = self.data[self.current_step]['close']
        
        obs = np.array([
            self.balance / self.initial_balance,
            self.shares_held,
            current_price,
            self.data[self.current_step].get('rsi', 50) / 100,
            self.data[self.current_step].get('macd', 0),
            # Add more features as needed
        ] + [0] * 10, dtype=np.float32)[:15]
        
        return obs
    
    def step(self, action):
        """Execute one time step"""
        current_price = self.data[self.current_step]['close']
        
        # Execute action
        if action == 1:  # BUY
            shares_to_buy = int(self.balance / current_price)
            if shares_to_buy > 0:
                self.shares_held += shares_to_buy
                self.balance -= shares_to_buy * current_price
        
        elif action == 2:  # SELL
            if self.shares_held > 0:
                self.balance += self.shares_held * current_price
                self.total_shares_sold += self.shares_held
                self.total_sales_value += self.shares_held * current_price
                self.shares_held = 0
        
        # Move to next step
        self.current_step += 1
        
        # Calculate reward (portfolio value change)
        portfolio_value = self.balance + self.shares_held * current_price
        reward = (portfolio_value - self.initial_balance) / self.initial_balance
        
        # Check if episode is done
        done = self.current_step >= len(self.data) - 1
        truncated = False
        
        return self._get_observation(), reward, done, truncated, {}
    
    def render(self):
        """Render environment (optional)"""
        pass

class RLTradingAgent:
    """RL agent for trading decisions"""
    
    def __init__(self, model_path: str = "data/models/rl_agent.zip"):
        self.model_path = Path(model_path)
        self.model = None
    
    def train(self, env, total_timesteps: int = 10000):
        """Train the RL agent"""
        vec_env = DummyVecEnv([lambda: env])
        
        self.model = PPO(
            "MlpPolicy",
            vec_env,
            verbose=1,
            learning_rate=0.0003,
            n_steps=2048,
            batch_size=64,
            n_epochs=10
        )
        
        logger.info("Starting RL agent training...")
        self.model.learn(total_timesteps=total_timesteps)
        logger.info("RL training completed")
    
    def predict(self, observation):
        """Get trading action from agent"""
        if self.model is None:
            self.load_model()
        
        action, _states = self.model.predict(observation, deterministic=True)
        return action
    
    def save_model(self):
        """Save trained model"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        self.model.save(self.model_path)
        logger.info(f"RL model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model"""
        if self.model_path.exists():
            self.model = PPO.load(self.model_path)
            logger.info("RL model loaded successfully")
        else:
            logger.warning("No saved RL model found")
