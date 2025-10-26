"""
Currency and localization utilities for Indian market
"""

def format_inr(amount: float) -> str:
    """
    Format amount in Indian Rupee format
    Example: 150000.50 -> ₹1,50,000.50
    """
    if amount >= 10000000:  # 1 Crore or more
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 Lakh or more
        return f"₹{amount/100000:.2f} L"
    else:
        return f"₹{amount:,.2f}"

def parse_inr_string(amount_str: str) -> float:
    """
    Parse INR formatted string to float
    Example: "₹1,50,000.50" -> 150000.50
    """
    cleaned = amount_str.replace('₹', '').replace(',', '').strip()
    if 'Cr' in cleaned:
        return float(cleaned.replace('Cr', '').strip()) * 10000000
    elif 'L' in cleaned:
        return float(cleaned.replace('L', '').strip()) * 100000
    else:
        return float(cleaned)

# Currency configuration
CURRENCY_CONFIG = {
    "symbol": "₹",
    "code": "INR",
    "name": "Indian Rupee",
    "decimal_places": 2,
    "thousand_separator": ",",
    "decimal_separator": ".",
}

# Indian number formatting
def indian_number_format(num: float) -> str:
    """
    Format numbers in Indian system (Lakhs, Crores)
    """
    if num >= 10000000:  # >= 1 Crore
        return f"{num/10000000:.2f} Cr"
    elif num >= 100000:  # >= 1 Lakh
        return f"{num/100000:.2f} L"
    elif num >= 1000:  # >= 1 Thousand
        return f"{num/1000:.2f} K"
    else:
        return f"{num:.2f}"