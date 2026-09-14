import argparse
import requests

def get_rates():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        response.raise_for_status()
        data = response.json()
        return data['rates']
    except requests.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None

def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency not in rates or to_currency not in rates:
        raise ValueError("Unsupported currency code.")
    
    # Convert to USD first, then to target currency
    usd_amount = amount / rates[from_currency]
    converted_amount = usd_amount * rates[to_currency]
    return converted_amount

def main():
    rates = get_rates()
    if rates is None:
        return

    parser = argparse.ArgumentParser(description='Currency Translator')
    parser.add_argument('--amount', type=float, required=True, help='Amount to convert')
    parser.add_argument('--from', dest='from_currency', type=str, required=True, help='Source currency (e.g., USD)')
    parser.add_argument('--to', dest='to_currency', type=str, required=True, help='Target currency (e.g., EUR)')

    args = parser.parse_args()

    from_curr = args.from_currency.upper()
    to_curr = args.to_currency.upper()

    if from_curr not in rates or to_curr not in rates:
        print(f"Error: Unsupported currency. Supported currencies are available via the API.")
        return

    try:
        converted_amount = convert_currency(args.amount, from_curr, to_curr, rates)
        print(f"{args.amount} {from_curr} = {converted_amount:.2f} {to_curr}")
    except ValueError as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    main()