import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ArrowUpRight, ArrowDownRight } from "lucide-react";

const trades = [
  { time: "14:32", symbol: "AAPL", type: "BUY", shares: 50, price: 150.32, pnl: null },
  { time: "13:45", symbol: "MSFT", type: "SELL", shares: 30, price: 378.91, pnl: 427.50 },
  { time: "12:18", symbol: "GOOGL", type: "BUY", shares: 25, price: 138.45, pnl: null },
  { time: "11:03", symbol: "NVDA", type: "SELL", shares: 20, price: 502.30, pnl: 986.00 },
  { time: "10:21", symbol: "TSLA", type: "BUY", shares: 15, price: 238.50, pnl: null },
  { time: "09:47", symbol: "META", type: "SELL", shares: 18, price: 331.20, pnl: -124.20 },
  { time: "09:15", symbol: "AMZN", type: "BUY", shares: 40, price: 147.65, pnl: null },
];

export const TradeHistory = () => {
  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-border/50 h-full">
      <CardHeader>
        <CardTitle>Recent Trades</CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[400px] pr-4">
          <div className="space-y-3">
            {trades.map((trade, index) => (
              <div
                key={index}
                className="p-3 rounded-lg border border-border/50 bg-card/50 hover:bg-muted/30 transition-all"
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <div className={`p-1 rounded ${
                      trade.type === "BUY" 
                        ? "bg-success/20" 
                        : "bg-destructive/20"
                    }`}>
                      {trade.type === "BUY" ? (
                        <ArrowUpRight className="h-4 w-4 text-success" />
                      ) : (
                        <ArrowDownRight className="h-4 w-4 text-destructive" />
                      )}
                    </div>
                    <div>
                      <div className="font-bold text-sm">{trade.symbol}</div>
                      <div className="text-xs text-muted-foreground">{trade.time}</div>
                    </div>
                  </div>
                  <Badge
                    variant={trade.type === "BUY" ? "default" : "secondary"}
                    className={trade.type === "BUY" ? "bg-success" : ""}
                  >
                    {trade.type}
                  </Badge>
                </div>
                
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-muted-foreground">Shares:</span>
                    <span className="ml-1 font-medium">{trade.shares}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Price:</span>
                    <span className="ml-1 font-medium">${trade.price}</span>
                  </div>
                </div>
                
                {trade.pnl !== null && (
                  <div className="mt-2 pt-2 border-t border-border/30">
                    <span className="text-xs text-muted-foreground">P&L: </span>
                    <span className={`text-xs font-semibold ${
                      trade.pnl >= 0 ? "text-success" : "text-destructive"
                    }`}>
                      {trade.pnl >= 0 ? "+" : ""}${trade.pnl.toFixed(2)}
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};
