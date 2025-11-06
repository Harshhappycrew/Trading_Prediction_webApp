import { useState } from "react";
import { StockSelector } from "@/components/dashboard/StockSelector";
import { formatINR } from "@/utils/currency";
import { TrendingUp, TrendingDown, Activity, DollarSign, Target, AlertCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PortfolioChart } from "@/components/dashboard/PortfolioChart";
import { PositionsTable } from "@/components/dashboard/PositionsTable";
import { TradeHistory } from "@/components/dashboard/TradeHistory";
import { MetricsGrid } from "@/components/dashboard/MetricsGrid";
import { PriceChart } from "@/components/dashboard/PriceChart";
import { SignalIndicator } from "@/components/dashboard/SignalIndicator";

const Index = () => {
  const [selectedStock, setSelectedStock] = useState("RELIANCE");

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
              QuantEdge Dashboard
            </h1>
            <p className="text-muted-foreground mt-2">
              AI-Powered Trading Simulator - NSE India
            </p>
          </div>
        </div>

        <StockSelector onStockChange={setSelectedStock} />

        <MetricsGrid symbol={selectedStock} />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <PortfolioChart />
          <PriceChart symbol={selectedStock} />
        </div>

        <SignalIndicator symbol={selectedStock} />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <PositionsTable />
          <TradeHistory />
        </div>
      </div>
    </div>
  );
};

export default Index;
