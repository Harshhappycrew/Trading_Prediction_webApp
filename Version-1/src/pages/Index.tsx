import { useState } from "react";
import { TrendingUp, TrendingDown, Activity, DollarSign, Target, AlertCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PortfolioChart } from "@/components/dashboard/PortfolioChart";
import { PositionsTable } from "@/components/dashboard/PositionsTable";
import { TradeHistory } from "@/components/dashboard/TradeHistory";
import { MetricsGrid } from "@/components/dashboard/MetricsGrid";
import { PriceChart } from "@/components/dashboard/PriceChart";
import { SignalIndicator } from "@/components/dashboard/SignalIndicator";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Activity className="h-8 w-8 text-primary" />
            <h1 className="text-2xl font-bold tracking-tight">QuantEdge</h1>
            <span className="text-xs text-muted-foreground">AI Trading Simulator</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-sm text-muted-foreground">Portfolio Value</div>
              <div className="text-xl font-bold text-success">$125,847.92</div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 space-y-6">
        {/* Metrics Grid */}
        <MetricsGrid />

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <PortfolioChart />
          <PriceChart />
        </div>

        {/* ML Signal Indicator */}
        <SignalIndicator />

        {/* Positions and History */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          <div className="xl:col-span-2">
            <PositionsTable />
          </div>
          <div>
            <TradeHistory />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
