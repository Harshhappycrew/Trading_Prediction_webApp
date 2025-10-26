import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown } from "lucide-react";

const positions = [
  { symbol: "AAPL", shares: 150, avgPrice: 145.32, currentPrice: 150.32, pnl: 750, pnlPercent: 3.44 },
  { symbol: "GOOGL", shares: 75, avgPrice: 135.20, currentPrice: 138.45, pnl: 243.75, pnlPercent: 2.40 },
  { symbol: "MSFT", shares: 100, avgPrice: 368.50, currentPrice: 378.91, pnl: 1041, pnlPercent: 2.83 },
  { symbol: "TSLA", shares: 50, avgPrice: 245.80, currentPrice: 238.50, pnl: -365, pnlPercent: -2.97 },
  { symbol: "NVDA", shares: 80, avgPrice: 485.00, currentPrice: 502.30, pnl: 1384, pnlPercent: 3.57 },
  { symbol: "META", shares: 60, avgPrice: 325.40, currentPrice: 331.20, pnl: 348, pnlPercent: 1.78 },
  { symbol: "AMZN", shares: 90, avgPrice: 142.80, currentPrice: 147.65, pnl: 436.50, pnlPercent: 3.40 },
];

export const PositionsTable = () => {
  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-border/50">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Active Positions</span>
          <Badge variant="outline">{positions.length} holdings</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="rounded-lg border border-border/50 overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="bg-secondary/50">
                <TableHead className="font-semibold">Symbol</TableHead>
                <TableHead className="text-right font-semibold">Shares</TableHead>
                <TableHead className="text-right font-semibold">Avg Price</TableHead>
                <TableHead className="text-right font-semibold">Current</TableHead>
                <TableHead className="text-right font-semibold">P&L</TableHead>
                <TableHead className="text-right font-semibold">Return</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {positions.map((position) => (
                <TableRow key={position.symbol} className="hover:bg-muted/30 transition-colors">
                  <TableCell className="font-bold text-foreground">{position.symbol}</TableCell>
                  <TableCell className="text-right">{position.shares}</TableCell>
                  <TableCell className="text-right text-muted-foreground">
                    ${position.avgPrice.toFixed(2)}
                  </TableCell>
                  <TableCell className="text-right font-medium">
                    ${position.currentPrice.toFixed(2)}
                  </TableCell>
                  <TableCell className="text-right">
                    <span className={position.pnl >= 0 ? "text-success font-semibold" : "text-destructive font-semibold"}>
                      {position.pnl >= 0 ? "+" : ""}${position.pnl.toFixed(2)}
                    </span>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex items-center justify-end gap-1">
                      {position.pnlPercent >= 0 ? (
                        <TrendingUp className="h-4 w-4 text-success" />
                      ) : (
                        <TrendingDown className="h-4 w-4 text-destructive" />
                      )}
                      <span className={position.pnlPercent >= 0 ? "text-success font-semibold" : "text-destructive font-semibold"}>
                        {position.pnlPercent >= 0 ? "+" : ""}{position.pnlPercent.toFixed(2)}%
                      </span>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
};
