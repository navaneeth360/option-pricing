# Helper function to return required data given a ticker symbol
# Values found from historic data : Spot price, Volatility
# Values found from option data : Strike prices, time to expiry, Option prices
# Returns a dictionary with calls, puts, strike prices, expiry date, volatility, time to expiry, spot price

import numpy as np
import datetime
import yfinance as yf
from .yfin import Ticker

# def get_option_prices(stock, expiry_date = None):
#     # Fetch option chain data
#     option_chain = stock.option_chain(expiry_date)

#     print(option_chain.calls.head())

#     strike_prices_c = option_chain.calls['strike'].unique()
#     strike_prices_p = option_chain.puts['strike'].unique()
#     strike_prices = list(set(strike_prices_c) & set(strike_prices_p))
#     strike_prices.sort()

#     print("Strike prices:", strike_prices)

#     call_prices = option_chain.calls[option_chain.calls['strike'].isin(strike_prices)]['lastPrice'].values
#     put_prices = option_chain.puts[option_chain.puts['strike'].isin(strike_prices)]['lastPrice'].values

#     return {
#         'calls': call_prices,
#         'puts': put_prices,
#         'strike_prices': strike_prices,
#         'expiry_date': expiry_date
#     }

def get_option_prices(stock, expiry_date = None):
    # Fetch option chain data
    option_chain = stock.option_chain(expiry_date)

    print(option_chain.calls.head())

    strike_prices_c = option_chain.calls['strike'].unique()
    strike_prices_p = option_chain.puts['strike'].unique()
    strike_prices = list(set(strike_prices_c) | set(strike_prices_p))
    strike_prices.sort()

    print("Strike prices:", strike_prices)

    call_prices = option_chain.calls[option_chain.calls['strike'].isin(strike_prices)]['lastPrice'].values
    put_prices = option_chain.puts[option_chain.puts['strike'].isin(strike_prices)]['lastPrice'].values

    return {
        'calls': call_prices,
        'puts': put_prices,
        'strike_prices': strike_prices,
        'strike_prices_c': strike_prices_c,
        'strike_prices_p': strike_prices_p,
        'expiry_date': expiry_date
    }


def get_option_data(ticker, time_to_expiry=None):
    """
    Fetches option data for a given ticker symbol.
    
    Parameters:
    ticker (str): The ticker symbol of the stock.
    
    Returns:
    dict: A dictionary containing option data including strike prices, time to expiry, and option prices.
    """
    stock = yf.Ticker(ticker)
    options = stock.options
    if not options:
        raise ValueError(f"No options available for ticker {ticker}")
    
    # Get the nearest expiry date
    if (time_to_expiry is None):
        # Get latest expiry date if no specific time to expiry is provided
        expiry_date = options[0]
        expiry_date_f = datetime.datetime.strptime(expiry_date, '%Y-%m-%d').date()
    else:
        # Find the nearest expiry date based on the provided time to expiry
        target_date = datetime.date.today() + datetime.timedelta(days=time_to_expiry)
        # Convert all option expiry dates to date objects
        expiry_dates = [datetime.datetime.strptime(opt, '%Y-%m-%d').date() for opt in options]
        # Find the expiry date with the minimum difference to target_date
        expiry_date_f = min(expiry_dates, key=lambda d: abs((d - target_date).days))
        expiry_date = expiry_date_f.strftime('%Y-%m-%d')

    # Get the time to expiry in days
    today = datetime.date.today()
    time_to_expiry = (expiry_date_f - today).days

    print("Time to expiry of nearest option:", time_to_expiry, "days")
    
    # Fetch the option chain for the nearest expiry date
    price_lists = get_option_prices(stock, expiry_date)

    print("Call prices:", price_lists['calls'])

    # To calculate volatility, we need the historical data
    historical_data = Ticker.get_past_data(ticker)
    spot_price = historical_data['Adj Close'].iloc[-1]
    adj_close = historical_data['Adj Close']
    log_returns = np.log(adj_close / adj_close.shift(1))
    volatility = np.std(log_returns.dropna()) * np.sqrt(252)  # Annualized volatility

    print("Volatility:", volatility)

    price_lists['volatility'] = volatility
    price_lists['time_to_expiry'] = time_to_expiry
    price_lists['spot_price'] = spot_price

    return price_lists


#get_option_data('AAPL')  # Example usage

