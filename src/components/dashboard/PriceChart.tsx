import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

// Generate sample price data with ML prediction
const generatePriceData = () => {
  const data = [];
  let price = 150;
  for (let i = 0; i < 20; i++) {
    const actual = price + (Math.random() - 0.5) * 5;
    const predicted = actual + (Math.random() - 0.5) * 2;
    data.push({
      time: `${9 + Math.floor(i / 2)}:${i % 2 === 0 ? '00' : '30'}`,
      actual: Math.round(actual * 100) / 100,
      predicted: Math.round(predicted * 100) / 100,
      upperBound: Math.round((predicted + 2) * 100) / 100,
      lowerBound: Math.round((predicted - 2) * 100) / 100,
    });
    price = actual;
  }
  return data;
};

const data = generatePriceData();

export const PriceChart = () => {
  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-border/50">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div>
            <span>AAPL Price Prediction</span>
            <div className="text-sm font-normal text-muted-foreground mt-1">LSTM Model Forecast</div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-foreground">${data[data.length - 1].actual}</div>
            <div className="text-xs text-success">+2.4%</div>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
            <XAxis 
              dataKey="time" 
              stroke="hsl(var(--muted-foreground))"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              stroke="hsl(var(--muted-foreground))"
              style={{ fontSize: '12px' }}
              domain={['dataMin - 2', 'dataMax + 2']}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '8px',
                color: 'hsl(var(--foreground))',
              }}
            />
            <Line
              type="monotone"
              dataKey="upperBound"
              stroke="hsl(var(--muted-foreground))"
              strokeWidth={1}
              dot={false}
              strokeDasharray="2 2"
              opacity={0.3}
            />
            <Line
              type="monotone"
              dataKey="lowerBound"
              stroke="hsl(var(--muted-foreground))"
              strokeWidth={1}
              dot={false}
              strokeDasharray="2 2"
              opacity={0.3}
            />
            <Line
              type="monotone"
              dataKey="predicted"
              stroke="hsl(var(--warning))"
              strokeWidth={2}
              dot={{ fill: 'hsl(var(--warning))', r: 3 }}
              name="ML Prediction"
            />
            <Line
              type="monotone"
              dataKey="actual"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              dot={{ fill: 'hsl(var(--primary))', r: 3 }}
              name="Actual Price"
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};
