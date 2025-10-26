import { TrendingUp, TrendingDown, DollarSign, Target, Activity, AlertCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { formatINR } from '@/utils/currency';

const metrics = [
  {
    label: "Total P&L",
    value: formatINR(25847.92),
    change: "+25.8%",
    positive: true,
    icon: DollarSign,
    glow: true,
  },
  {
    label: "Sharpe Ratio",
    value: "1.87",
    change: "Excellent",
    positive: true,
    icon: Target,
  },
  {
    label: "Win Rate",
    value: "64.2%",
    change: "+2.1%",
    positive: true,
    icon: TrendingUp,
  },
  {
    label: "Max Drawdown",
    value: "-8.3%",
    change: "Within Limit",
    positive: true,
    icon: AlertCircle,
  },
  {
    label: "Active Positions",
    value: "7",
    change: "3 signals",
    positive: true,
    icon: Activity,
  },
  {
    label: "Sortino Ratio",
    value: "2.14",
    change: "Strong",
    positive: true,
    icon: TrendingUp,
  },
];

export const MetricsGrid = () => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
      {metrics.map((metric, index) => {
        const Icon = metric.icon;
        return (
          <Card 
            key={index} 
            className={`bg-gradient-to-br from-card to-secondary/30 border-border/50 transition-all hover:border-primary/50 ${
              metric.glow ? 'glow-success' : ''
            }`}
          >
            <CardContent className="p-4">
              <div className="flex items-start justify-between mb-2">
                <Icon className={`h-4 w-4 ${metric.positive ? 'text-success' : 'text-destructive'}`} />
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  metric.positive ? 'bg-success/20 text-success' : 'bg-destructive/20 text-destructive'
                }`}>
                  {metric.change}
                </span>
              </div>
              <div className="space-y-1">
                <p className="text-2xl font-bold tracking-tight">{metric.value}</p>
                <p className="text-xs text-muted-foreground">{metric.label}</p>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
};
