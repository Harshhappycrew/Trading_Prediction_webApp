import { useState, useEffect } from "react";
import { Search, TrendingUp } from "lucide-react";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface StockOption {
  ticker: string;
  name: string;
  display: string;
}

interface StockSelectorProps {
  onStockChange: (stock: string) => void;
  initialStock?: string;
}

export const StockSelector = ({ 
  onStockChange, 
  initialStock = "RELIANCE" 
}: StockSelectorProps) => {
  const [stocks, setStocks] = useState<StockOption[]>([]);
  const [selectedStock, setSelectedStock] = useState(initialStock);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/stocks/all");
        const data = await response.json();
        setStocks(data.stocks);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching stocks:", error);
        setStocks([
          { ticker: "RELIANCE", name: "Reliance Industries Ltd", display: "RELIANCE - Reliance Industries" },
          { ticker: "TCS", name: "Tata Consultancy Services", display: "TCS - Tata Consultancy Services" },
          { ticker: "HDFCBANK", name: "HDFC Bank", display: "HDFCBANK - HDFC Bank" },
        ]);
        setIsLoading(false);
      }
    };

    fetchStocks();
  }, []);

  const handleStockChange = (value: string) => {
    setSelectedStock(value);
    onStockChange(value);
  };

  const filteredStocks = stocks.filter((stock) =>
    stock.ticker.toLowerCase().includes(searchQuery.toLowerCase()) ||
    stock.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Card className="p-4 bg-card/50 backdrop-blur">
      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search stocks (e.g., RELIANCE, TCS)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

        <Select 
          value={selectedStock} 
          onValueChange={handleStockChange}
          disabled={isLoading}
        >
          <SelectTrigger className="w-[280px]">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              <SelectValue placeholder="Select stock" />
            </div>
          </SelectTrigger>
          <SelectContent className="max-h-[400px]">
            {filteredStocks.length > 0 ? (
              filteredStocks.map((stock) => (
                <SelectItem key={stock.ticker} value={stock.ticker}>
                  <div className="flex items-center justify-between w-full">
                    <span className="font-semibold">{stock.ticker}</span>
                    <span className="text-xs text-muted-foreground ml-2">
                      {stock.name}
                    </span>
                  </div>
                </SelectItem>
              ))
            ) : (
              <div className="p-4 text-center text-muted-foreground">
                No stocks found
              </div>
            )}
          </SelectContent>
        </Select>

        <Badge variant="secondary" className="text-sm">
          Selected: {selectedStock}
        </Badge>
      </div>
    </Card>
  );
};