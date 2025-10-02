
from forex_python.converter import CurrencyRates

c = CurrencyRates()
SUPPORTED_CURRENCIES = ["INR", "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF"]

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Convert amount from one currency to another using forex-python.
    Returns the converted amount rounded to 2 decimals.
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    if from_currency == to_currency:
        return amount

    try:
        converted_amount = c.convert(from_currency, to_currency, amount)
        return round(converted_amount, 2)
    except Exception as e:
        print(f"Currency conversion failed: {e}")
        # fallback to original amount if API fails
        return amount
