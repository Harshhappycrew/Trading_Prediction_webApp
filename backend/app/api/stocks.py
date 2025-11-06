"""
Indian Stock Market (NSE/BSE) API
All prices in INR (₹)
"""
from fastapi import APIRouter, Query, HTTPException
import yfinance as yf
from typing import List, Dict
from app.uitls.currency import format_inr, indian_number_format

router = APIRouter()

INDIAN_STOCKS_DATABASE = {
    # Nifty 50 - Top Blue Chip Companies
    "RELIANCE": "Reliance Industries Limited",
    "TCS": "Tata Consultancy Services Limited",
    "HDFCBANK": "HDFC Bank Limited",
    "INFY": "Infosys Limited",
    "ICICIBANK": "ICICI Bank Limited",
    "BHARTIARTL": "Bharti Airtel Limited",
    "SBIN": "State Bank of India",
    "HINDUNILVR": "Hindustan Unilever Limited",
    "ITC": "ITC Limited",
    "LT": "Larsen & Toubro Limited",
    "BAJFINANCE": "Bajaj Finance Limited",
    "KOTAKBANK": "Kotak Mahindra Bank Limited",
    "HCLTECH": "HCL Technologies Limited",
    "AXISBANK": "Axis Bank Limited",
    "MARUTI": "Maruti Suzuki India Limited",
    "SUNPHARMA": "Sun Pharmaceutical Industries Limited",
    "TITAN": "Titan Company Limited",
    "ULTRACEMCO": "UltraTech Cement Limited",
    "ASIANPAINT": "Asian Paints Limited",
    "WIPRO": "Wipro Limited",
    "NESTLEIND": "Nestle India Limited",
    "BAJAJ-AUTO": "Bajaj Auto Limited",
    "M&M": "Mahindra & Mahindra Limited",
    "TATASTEEL": "Tata Steel Limited",
    "TATAMOTORS": "Tata Motors Limited",
    "NTPC": "NTPC Limited",
    "POWERGRID": "Power Grid Corporation of India Limited",
    "COALINDIA": "Coal India Limited",
    "ADANIPORTS": "Adani Ports and Special Economic Zone Limited",
    "JSWSTEEL": "JSW Steel Limited",
    "TECHM": "Tech Mahindra Limited",
    "ONGC": "Oil and Natural Gas Corporation Limited",
    "HINDALCO": "Hindalco Industries Limited",
    "INDUSINDBK": "IndusInd Bank Limited",
    "GRASIM": "Grasim Industries Limited",
    "BAJAJFINSV": "Bajaj Finserv Limited",
    "EICHERMOT": "Eicher Motors Limited",
    "CIPLA": "Cipla Limited",
    "BRITANNIA": "Britannia Industries Limited",
    "APOLLOHOSP": "Apollo Hospitals Enterprise Limited",
    "DIVISLAB": "Divi's Laboratories Limited",
    "DRREDDY": "Dr. Reddy's Laboratories Limited",
    "HEROMOTOCO": "Hero MotoCorp Limited",
    "SHRIRAMFIN": "Shriram Finance Limited",
    "JIOFIN": "Jio Financial Services Limited",
    "TATACONSUM": "Tata Consumer Products Limited",
    "TRENT": "Trent Limited",
    "ADANIENT": "Adani Enterprises Limited",
    "BEL": "Bharat Electronics Limited",
    
    # Banking & Financial Services
    "PNB": "Punjab National Bank",
    "BANKBARODA": "Bank of Baroda",
    "BANKINDIA": "Bank of India",
    "CANBK": "Canara Bank",
    "INDIANB": "Indian Bank",
    "FEDERALBNK": "Federal Bank Limited",
    "IDFCFIRSTB": "IDFC First Bank Limited",
    "BANDHANBNK": "Bandhan Bank Limited",
    "AUBANK": "AU Small Finance Bank Limited",
    "CHOLAFIN": "Cholamandalam Investment and Finance Company Limited",
    "SBILIFE": "SBI Life Insurance Company Limited",
    "HDFCLIFE": "HDFC Life Insurance Company Limited",
    "ICICIGI": "ICICI Lombard General Insurance Company Limited",
    "ICICIPRULI": "ICICI Prudential Life Insurance Company Limited",
    "MFSL": "Max Financial Services Limited",
    "HDFCAMC": "HDFC Asset Management Company Limited",
    
    # IT & Technology
    "LTIM": "LTIMindtree Limited",
    "MPHASIS": "MphasiS Limited",
    "COFORGE": "Coforge Limited",
    "PERSISTENT": "Persistent Systems Limited",
    "KPITTECH": "KPIT Technologies Limited",
    
    # Pharmaceuticals & Healthcare
    "BIOCON": "Biocon Limited",
    "LUPIN": "Lupin Limited",
    "AUROPHARMA": "Aurobindo Pharma Limited",
    "TORNTPHARM": "Torrent Pharmaceuticals Limited",
    "ALKEM": "Alkem Laboratories Limited",
    "MANKIND": "Mankind Pharma Limited",
    "LAURUSLABS": "Laurus Labs Limited",
    "GLENMARK": "Glenmark Pharmaceuticals Limited",
    "FORTIS": "Fortis Healthcare Limited",
    "MAXHEALTH": "Max Healthcare Institute Limited",
    
    # Automotive & Auto Components
    "TVSMOTOR": "TVS Motor Company Limited",
    "ASHOKLEY": "Ashok Leyland Limited",
    "MOTHERSON": "Samvardhana Motherson International Limited",
    "BOSCHLTD": "Bosch Limited",
    "MRF": "MRF Limited",
    "BHARATFORG": "Bharat Forge Limited",
    "EXIDEIND": "Exide Industries Limited",
    "AMARAJABAT": "Amara Raja Energy & Mobility Limited",
    
    # FMCG & Consumer Goods
    "DABUR": "Dabur India Limited",
    "MARICO": "Marico Limited",
    "GODREJCP": "Godrej Consumer Products Limited",
    "COLPAL": "Colgate Palmolive (India) Limited",
    "EMAMILTD": "Emami Limited",
    "VBL": "Varun Beverages Limited",
    "JUBLFOOD": "Jubilant Foodworks Limited",
    
    # Retail & E-commerce
    "DMART": "Avenue Supermarts Limited",
    "NYKAA": "FSN E-Commerce Ventures Limited (Nykaa)",
    "ZOMATO": "Zomato Limited",
    "PAYTM": "One 97 Communications Limited (Paytm)",
    
    # Real Estate & Infrastructure
    "DLF": "DLF Limited",
    "GODREJPROP": "Godrej Properties Limited",
    "OBEROIRLTY": "Oberoi Realty Limited",
    "PRESTIGE": "Prestige Estates Projects Limited",
    "PHOENIXLTD": "Phoenix Mills Limited",
    "LODHA": "Lodha Developers Limited",
    
    # Cement & Construction Materials
    "AMBUJACEM": "Ambuja Cements Limited",
    "ACC": "ACC Limited",
    "SHREECEM": "Shree Cement Limited",
    "DALBHARAT": "Dalmia Bharat Limited",
    "JKCEMENT": "JK Cement Limited",
    
    # Energy & Power
    "BPCL": "Bharat Petroleum Corporation Limited",
    "IOC": "Indian Oil Corporation Limited",
    "HINDPETRO": "Hindustan Petroleum Corporation Limited",
    "ADANIGREEN": "Adani Green Energy Limited",
    "ADANIPOWER": "Adani Power Limited",
    "TATAPOWER": "Tata Power Company Limited",
    "NHPC": "NHPC Limited",
    "SJVN": "SJVN Limited",
    "PFC": "Power Finance Corporation Limited",
    "RECLTD": "REC Limited",
    
    # Metals & Mining
    "VEDL": "Vedanta Limited",
    "NMDC": "NMDC Limited",
    "HINDZINC": "Hindustan Zinc Limited",
    "NATIONALUM": "National Aluminium Company Limited",
    "SAIL": "Steel Authority of India Limited",
    "JINDALSTEL": "Jindal Steel & Power Limited",
    "RATNAMANI": "Ratnamani Metals & Tubes Limited",
    
    # Chemicals & Fertilizers
    "UPL": "UPL Limited",
    "PIIND": "PI Industries Limited",
    "AARTI": "Aarti Industries Limited",
    "DEEPAKNTR": "Deepak Nitrite Limited",
    "SRF": "SRF Limited",
    "BALRAMCHIN": "Balrampur Chini Mills Limited",
    
    # Logistics & Transportation
    "CONCOR": "Container Corporation of India Limited",
    "IRCTC": "Indian Railway Catering and Tourism Corporation Limited",
    "VRL": "VRL Logistics Limited",
    "MAHLOG": "Mahindra Logistics Limited",
    "BLUEDART": "Blue Dart Express Limited",
    
    # Capital Goods & Engineering
    "ABB": "ABB India Limited",
    "SIEMENS": "Siemens Limited",
    "HAVELLS": "Havells India Limited",
    "CROMPTON": "Crompton Greaves Consumer Electricals Limited",
    "VOLTAS": "Voltas Limited",
    "CUMMINSIND": "Cummins India Limited",
    "THERMAX": "Thermax Limited",
    
    # Textiles & Apparel
    "RAYMOND": "Raymond Limited",
    "ARVIND": "Arvind Limited",
    "PAGEIND": "Page Industries Limited",
    "GOKEX": "Gokaldas Exports Limited",
    
    # Media & Entertainment
    "ZEEL": "Zee Entertainment Enterprises Limited",
    "PVRINOX": "PVR INOX Limited",
    "SAREGAMA": "Saregama India Limited",
    "TIPS": "Tips Industries Limited",
    
    # Hotels & Tourism
    "INDIANHOTE": "Indian Hotels Company Limited",
    "LEMONTREE": "Lemon Tree Hotels Limited",
    "CHALET": "Chalet Hotels Limited",
    
    # Insurance
    "LICI": "Life Insurance Corporation Of India",
    
    # Defense & Aerospace
    "HAL": "Hindustan Aeronautics Limited",
    "BDL": "Bharat Dynamics Limited",
    "MAZDOCK": "Mazagon Dock Shipbuilders Limited",
    "GRSE": "Garden Reach Shipbuilders & Engineers Limited",
}

@router.get("/search")
async def search_indian_stocks(query: str = Query(..., min_length=1, max_length=50)):
    """
    Search for Indian stocks by ticker symbol or company name
    Example: GET /api/stocks/search?query=reliance
    """
    try:
        query_lower = query.lower()
        query_upper = query.upper()
        
        results = []
        for ticker, name in INDIAN_STOCKS_DATABASE.items():
            if query_upper in ticker or query_lower in name.lower():
                results.append({
                    "ticker": ticker,
                    "name": name,
                    "display": f"{ticker} - {name}",
                    "exchange": "NSE"
                })
        
        return {
            "query": query,
            "count": len(results),
            "results": results[:20],
            "currency": "INR"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all")
async def get_all_indian_stocks():
    """
    Get complete list of available Indian stocks
    Example: GET /api/stocks/all
    """
    try:
        stocks = [
            {
                "ticker": k,
                "name": v,
                "display": f"{k} - {v}",
                "exchange": "NSE"
            }
            for k, v in INDIAN_STOCKS_DATABASE.items()
        ]
        return {
            "count": len(stocks),
            "stocks": stocks,
            "currency": "INR",
            "exchange": "NSE"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info/{symbol}")
async def get_indian_stock_info(symbol: str):
    """
    Get detailed information about a specific Indian stock
    Example: GET /api/stocks/info/RELIANCE
    Returns prices in INR (₹)
    """
    try:
        symbol_upper = symbol.upper()
        
        # Check if stock exists in our database
        if symbol_upper not in INDIAN_STOCKS_DATABASE:
            raise HTTPException(
                status_code=404,
                detail=f"Stock {symbol_upper} not found in NSE database"
            )
        
        # Fetch real-time data from yfinance (NSE)
        nse_symbol = f"{symbol_upper}.NS"
        ticker = yf.Ticker(nse_symbol)
        info = ticker.info
        
        current_price = info.get("currentPrice", 0)
        market_cap = info.get("marketCap", 0)
        
        return {
            "symbol": symbol_upper,
            "name": INDIAN_STOCKS_DATABASE[symbol_upper],
            "exchange": "NSE",
            "currency": "INR",
            "current_price": current_price,
            "current_price_formatted": format_inr(current_price),
            "market_cap": market_cap,
            "market_cap_formatted": indian_number_format(market_cap),
            "day_high": info.get("dayHigh", 0),
            "day_low": info.get("dayLow", 0),
            "volume": info.get("volume", 0),
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "pe_ratio": info.get("trailingPE", 0),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def get_indian_stock_categories():
    """
    Get Indian stocks organized by sectors
    Example: GET /api/stocks/categories
    """
    categories = {
        "Banking & Finance": ["HDFCBANK", "ICICIBANK", "SBIN", "AXISBANK", "KOTAKBANK"],
        "IT & Technology": ["TCS", "INFY", "HCLTECH", "WIPRO", "TECHM"],
        "Automobiles": ["MARUTI", "M&M", "TATAMOTORS", "BAJAJ-AUTO", "HEROMOTOCO"],
        "FMCG": ["HINDUNILVR", "ITC", "NESTLEIND", "BRITANNIA", "DABUR"],
        "Pharma & Healthcare": ["SUNPHARMA", "DRREDDY", "CIPLA", "DIVISLAB", "APOLLOHOSP"],
        "Energy & Power": ["RELIANCE", "ONGC", "NTPC", "POWERGRID", "BPCL"],
        "Metals & Mining": ["TATASTEEL", "JSWSTEEL", "HINDALCO", "VEDL", "HINDZINC"],
        "Telecom": ["BHARTIARTL", "JIOFIN"],
    }
    
    result = {}
    for category, tickers in categories.items():
        result[category] = [
            {"ticker": t, "name": INDIAN_STOCKS_DATABASE.get(t, "Unknown")}
            for t in tickers if t in INDIAN_STOCKS_DATABASE
        ]
    
    return {
        "categories": result,
        "currency": "INR",
        "exchange": "NSE"
    }