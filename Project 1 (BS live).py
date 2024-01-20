
import yfinance as yf
from scipy.stats import norm
import numpy as np
import time
from datetime import datetime, timedelta

def download_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data['Adj Close']

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    return option_price

def real_time_option_pricing(symbol, strike_price, days_to_maturity, risk_free_rate, volatility):
    while True:
        try:
            # Get today's date
            today_date = datetime.now().strftime('%Y-%m-%d')

            # Download the latest stock price
            current_stock_price = download_stock_data(symbol + ".NS", today_date, today_date).iloc[-1]

            # Calculate time to maturity in years
            maturity_date = datetime.now() + timedelta(days=days_to_maturity)
            time_to_maturity = (maturity_date - datetime.now()).days / 365.0

            # Calculate option price using the Black-Scholes model
            call_option_price = black_scholes(current_stock_price, strike_price, time_to_maturity, risk_free_rate, volatility, option_type='call')
            put_option_price = black_scholes(current_stock_price, strike_price, time_to_maturity, risk_free_rate, volatility, option_type='put')

            # Print or use the option prices as needed
            print(f"Today's Date: {today_date}")
            print(f"Stock Price: {current_stock_price}")
            print(f"Call Option Price: {call_option_price}")
            print(f"Put Option Price: {put_option_price}")

            # Sleep for a certain interval (e.g., 1 minute) before updating again
            time.sleep(60)

        except Exception as e:
            print(f"Error: {e}")
            # Handle errors, such as network issues or invalid data
            # Optionally, you can add more sophisticated error handling and logging
            time.sleep(60)

# Replace these values with your own
symbol = 'IRCTC'
strike_price = 150
days_to_maturity = 30
risk_free_rate = 0.06
volatility = 0.2  # You may need to estimate this based on historical data

real_time_option_pricing(symbol, strike_price, days_to_maturity, risk_free_rate, volatility)
