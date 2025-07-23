# Binomial Tree Model for option pricing

import numpy as np
from .framework import OptionModel
from scipy.stats import norm

class BTModel(OptionModel):
    def __init__(self, underlying_price, strike_price, time_to_maturity, risk_free_rate, volatility, time_steps):
        """
        Initializes the necessary variables for the Black-Scholes Model.

        underlying_price => Current price of the underlying asset
        strike_price => Strike price of the option
        time_to_maturity => Time to maturity in days
        risk_free_rate => Risk-free interest rate (annualized)
        volatility => Volatility of the underlying asset (annualized)
        time_steps => Number of time steps in the binomial tree
        """

        # Renaming them to familiar symbols 
        S = underlying_price
        self.K = strike_price
        T = time_to_maturity / 365 # Converting days to years
        self.r = risk_free_rate
        sigma = volatility
        self.n = time_steps
        self.delT = T / self.n  # Time step size

        # Defining up and down factors
        u = np.exp(sigma * np.sqrt(self.delT))
        d = 1.0 / u  

        # Vector to hold option prices at each node
        self.prices = np.zeros(self.n + 1)  # Array to hold prices at each node
        # Vector to hold underlying asset prices at maturity for all combinations of u and d
        self.S_vec = np.array([(S * u**j * d**(self.n - j)) for j in range(self.n + 1)])  

        # Risk-neutral probabilities
        a = np.exp(self.r * self.delT) 
        self.p = (a - d) / (u - d)
        self.q = 1.0 - self.p

    def _find_call_option_price(self):
        """
        Calculates price for call option according to the Binomial formula.
        """
        # Initializing call option prices at maturity
        self.prices[:] = np.maximum(self.S_vec - self.K, 0.0)

        # Backward induction to calculate option price at each node
        for i in range(self.n - 1, -1, -1):
            self.prices[:-1] = np.exp(-self.r * self.delT) * (self.p * self.prices[1:] + self.q * self.prices[:-1])

        return self.prices[0]
        
    def _find_put_option_price(self):
        """
        Calculates price for put option according to the Binomial formula.
        """
        # Initializing call option prices at maturity
        self.prices[:] = np.maximum(self.K - self.S_vec, 0.0)

        # Backward induction to calculate option price at each node
        for i in range(self.n - 1, -1, -1):
            self.prices[:-1] = np.exp(-self.r * self.delT) * (self.p * self.prices[1:] + self.q * self.prices[:-1])

        return self.prices[0]
        
