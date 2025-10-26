"""
Trading Simulation Engine
"""
from typing import Dict, List
from datetime import datetime
from loguru import logger

class TradingEngine:
    """Core trading simulation engine"""
    
    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
        self.cash_balance = initial_capital
        self.positions: Dict[str, Dict] = {}
        self.orders: List[Dict] = []
        self.trades: List[Dict] = []
        self.commission_rate = 0.001  # 0.1% commission
    
    def execute_order(self, symbol: str, action: str, quantity: int, price: float):
        """Execute a trading order"""
        try:
            commission = quantity * price * self.commission_rate
            
            if action.upper() == "BUY":
                total_cost = quantity * price + commission
                
                if total_cost > self.cash_balance:
                    logger.warning(f"Insufficient funds for {symbol} purchase")
                    return {"status": "rejected", "reason": "insufficient_funds"}
                
                # Update cash
                self.cash_balance -= total_cost
                
                # Update position
                if symbol in self.positions:
                    current_qty = self.positions[symbol]['quantity']
                    current_avg = self.positions[symbol]['avg_price']
                    new_qty = current_qty + quantity
                    new_avg = ((current_qty * current_avg) + (quantity * price)) / new_qty
                    
                    self.positions[symbol] = {
                        'quantity': new_qty,
                        'avg_price': new_avg,
                        'current_price': price
                    }
                else:
                    self.positions[symbol] = {
                        'quantity': quantity,
                        'avg_price': price,
                        'current_price': price
                    }
                
                trade = {
                    'symbol': symbol,
                    'action': 'BUY',
                    'quantity': quantity,
                    'price': price,
                    'commission': commission,
                    'timestamp': datetime.utcnow()
                }
                self.trades.append(trade)
                
                logger.info(f"BUY {quantity} {symbol} @ ${price:.2f}")
                return {"status": "filled", "trade": trade}
            
            elif action.upper() == "SELL":
                if symbol not in self.positions or self.positions[symbol]['quantity'] < quantity:
                    logger.warning(f"Insufficient shares for {symbol} sale")
                    return {"status": "rejected", "reason": "insufficient_shares"}
                
                # Calculate P&L
                avg_price = self.positions[symbol]['avg_price']
                pnl = (price - avg_price) * quantity - commission
                
                # Update cash
                self.cash_balance += quantity * price - commission
                
                # Update position
                self.positions[symbol]['quantity'] -= quantity
                if self.positions[symbol]['quantity'] == 0:
                    del self.positions[symbol]
                
                trade = {
                    'symbol': symbol,
                    'action': 'SELL',
                    'quantity': quantity,
                    'price': price,
                    'commission': commission,
                    'pnl': pnl,
                    'timestamp': datetime.utcnow()
                }
                self.trades.append(trade)
                
                logger.info(f"SELL {quantity} {symbol} @ ${price:.2f} (P&L: ${pnl:.2f})")
                return {"status": "filled", "trade": trade}
            
        except Exception as e:
            logger.error(f"Order execution error: {e}")
            return {"status": "error", "reason": str(e)}
    
    def update_prices(self, prices: Dict[str, float]):
        """Update current prices for all positions"""
        for symbol, price in prices.items():
            if symbol in self.positions:
                self.positions[symbol]['current_price'] = price
    
    def get_portfolio_value(self):
        """Calculate total portfolio value"""
        positions_value = sum(
            pos['quantity'] * pos['current_price']
            for pos in self.positions.values()
        )
        return self.cash_balance + positions_value
    
    def get_portfolio_metrics(self):
        """Get portfolio performance metrics"""
        total_value = self.get_portfolio_value()
        total_pnl = total_value - self.initial_capital
        total_pnl_percent = (total_pnl / self.initial_capital) * 100
        
        return {
            'total_value': total_value,
            'cash_balance': self.cash_balance,
            'positions_value': total_value - self.cash_balance,
            'total_pnl': total_pnl,
            'total_pnl_percent': total_pnl_percent,
            'num_positions': len(self.positions),
            'num_trades': len(self.trades)
        }
