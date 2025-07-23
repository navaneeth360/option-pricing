# Creating the Black Scholes Model for option pricing
# This model uses the Black-Scholes formula to calculate the price of a European call or put option

import numpy as np
from scipy.stats import norm
from .framework import OptionModel

class BSModel(OptionModel):
    def __init__(self, underlying_price, strike_price, time_to_maturity, risk_free_rate, volatility):
        """
        Initializes the necessary variables for the Black-Scholes Model.

        underlying_price => Current price of the underlying asset
        strike_price => Strike price of the option
        time_to_maturity => Time to maturity in days
        risk_free_rate => Risk-free interest rate (annualized)
        volatility => Volatility of the underlying asset (annualized)
        """

        # Renaming them to familiar symbols 
        S = underlying_price
        K = strike_price
        T = time_to_maturity / 365 # Converting days to years
        r = risk_free_rate
        sigma = volatility

        # Calculating d1 and d2 for the Black-Scholes formula
        self.d_1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        self.d_2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
        self.K_p = K * np.exp(-r * T) # Finding the present value of the strike price
        self.S = S
    
    def _find_call_option_price(self):
        """
        Calculates price of call option as 
        S * N(d1) - K_p * N(d2)
        """
        call_option_price = (self.S * norm.cdf(self.d_1, 0.0, 1.0) - self.K_p * norm.cdf(self.d_2, 0.0, 1.0))
        return call_option_price

    def _find_put_option_price(self):
        """
        Calculates price of put option as 
        K_p * N(-d2) - S * N(-d1)
        """
        put_option_price = (self.K_p * norm.cdf(-self.d_2, 0.0, 1.0) - self.S * norm.cdf(-self.d_1, 0.0, 1.0))
        return put_option_price