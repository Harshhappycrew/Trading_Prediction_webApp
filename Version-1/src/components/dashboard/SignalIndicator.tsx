import { Card, CardContent } from "@/components/ui/card";
import { TrendingUp, TrendingDown, Activity, Brain } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const signals = [
  {
    symbol: "AAPL",
    signal: "BUY",
    confidence: 87,
    model: "LSTM",
    reason: "Strong upward momentum, RSI oversold",
    price: "$150.32",
  },
  {
    symbol: "GOOGL",
    signal: "HOLD",
    confidence: 62,
    model: "Ensemble",
    reason: "Consolidating near resistance",
    price: "$138.45",
  },
  {
    symbol: "MSFT",
    signal: "BUY",
    confidence: 91,
    model: "RL Agent",
    reason: "Breakout above moving average",
    price: "$378.91",
  },
];

export const SignalIndicator = () => {
  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-border/50">
      <CardContent className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <Brain className="h-5 w-5 text-primary" />
          <h3 className="text-lg font-semibold">AI Trading Signals</h3>
          <Badge variant="outline" className="ml-auto">Real-time</Badge>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {signals.map((signal, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg border transition-all ${
                signal.signal === "BUY"
                  ? "bg-success/10 border-success/30 hover:border-success/50"
                  : signal.signal === "SELL"
                  ? "bg-destructive/10 border-destructive/30 hover:border-destructive/50"
                  : "bg-muted/10 border-border/30 hover:border-border/50"
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-lg font-bold">{signal.symbol}</span>
                  <span className="text-sm text-muted-foreground">{signal.price}</span>
                </div>
                {signal.signal === "BUY" ? (
                  <TrendingUp className="h-5 w-5 text-success" />
                ) : signal.signal === "SELL" ? (
                  <TrendingDown className="h-5 w-5 text-destructive" />
                ) : (
                  <Activity className="h-5 w-5 text-muted-foreground" />
                )}
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Badge
                    variant={
                      signal.signal === "BUY"
                        ? "default"
                        : signal.signal === "SELL"
                        ? "destructive"
                        : "secondary"
                    }
                    className="font-semibold"
                  >
                    {signal.signal}
                  </Badge>
                  <span className="text-sm font-medium">{signal.confidence}% confidence</span>
                </div>
                
                <div className="w-full bg-secondary rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      signal.signal === "BUY"
                        ? "bg-success"
                        : signal.signal === "SELL"
                        ? "bg-destructive"
                        : "bg-muted-foreground"
                    }`}
                    style={{ width: `${signal.confidence}%` }}
                  />
                </div>
                
                <div className="text-xs text-muted-foreground space-y-1">
                  <div className="flex items-center gap-1">
                    <span className="font-medium">Model:</span>
                    <span>{signal.model}</span>
                  </div>
                  <p>{signal.reason}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};
