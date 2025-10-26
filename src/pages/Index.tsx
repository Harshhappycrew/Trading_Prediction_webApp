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

const Index = () => { // (1) DECLARATION: functional component for the dashboard page
  const [selectedStock, setSelectedStock] = useState("RELIANCE"); // (2) STATE: local state hook holding the currently selected stock symbol

  return ( // (3) RENDER: start of JSX return
    <div className="min-h-screen bg-background p-6"> // (4) LAYOUT: page container with min height, background and padding
      <div className="max-w-7xl mx-auto space-y-6"> // (5) CENTERING: constrains width and vertically spaces child sections
        <div className="flex justify-between items-center mb-6"> // (6) HEADER ROW: flex layout aligning title and potential controls
          <div> // (7) TITLE CONTAINER
            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent"> // (8) MAIN TITLE styling with gradient text
              QuantEdge Dashboard // (9) TITLE TEXT
            </h1>
            <p className="text-muted-foreground mt-2"> // (10) SUBTITLE styling
              AI-Powered Trading Simulator - NSE India // (11) SUBTITLE TEXT
            </p>
          </div>
        </div>

        <StockSelector onStockChange={setSelectedStock} /> // (12) CONTROLLER: stock selector component; updates selectedStock via callback

        <MetricsGrid symbol={selectedStock} /> // (13) METRICS: displays KPIs/metrics for the selected symbol
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6"> // (14) TWO-COLUMN GRID: responsive container for charts
          <PortfolioChart /> // (15) CHART: user's portfolio performance chart (no props passed)
          <PriceChart symbol={selectedStock} /> // (16) CHART: price chart for the selected stock symbol
        </div>

        <SignalIndicator symbol={selectedStock} /> // (17) SIGNAL: shows buy/sell signals for the selected symbol

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6"> // (18) TWO-COLUMN GRID: for tables
          <PositionsTable /> // (19) TABLE: current open positions (no props passed)
          <TradeHistory /> // (20) TABLE: historical trades list
        </div>
      </div>
    </div>
  ); // (21) END RENDER
}; // (22) END COMPONENT

export default Index;
