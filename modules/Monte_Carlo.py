# Monte Carlo Model for option pricing

import numpy as np
from .framework import OptionModel
import matplotlib.pyplot as plt


class MCModel(OptionModel):
    def __init__(self, underlying_price, strike_price, time_to_maturity, risk_free_rate, volatility, number_of_simulations):
        """
        Initializes the necessary variables for the Black-Scholes Model.

        underlying_price => Current price of the underlying asset
        strike_price => Strike price of the option
        time_to_maturity => Time to maturity in days
        risk_free_rate => Risk-free interest rate (annualized)
        volatility => Volatility of the underlying asset (annualized)
        number_of_simulations => Number of simulations to run for Monte Carlo pricing
        """

        # Renaming them to familiar symbols 
        self.S0 = underlying_price
        self.K = strike_price
        self.T = time_to_maturity / 365 # Converting days to years
        self.r = risk_free_rate
        self.sigma = volatility

        self.N = number_of_simulations
        self.num_steps = time_to_maturity
        self.delT = self.T / self.num_steps
        self.sim_results = None

    def simulate_prices(self):
        """
        Simulates price movements of the underlying asset using a geometric Brownian motion model.
        """
        print("Simulating prices using Monte Carlo method...")
        np.random.seed(11)
        self.results = None
        # Initializing price movements rows as time index and columns as different random price movements.
        S = np.zeros((self.num_steps, self.N))
        # Starting value is the current spot price
        S[0] = self.S0

        for i in range(1, self.num_steps):
            # Random values selected from Gaussian distribution
            Z = np.random.standard_normal(self.N)
            # Updating prices for next point in time 
            S[i] = S[i - 1] * np.exp((self.r - 0.5 * self.sigma ** 2) * self.delT + (self.sigma * np.sqrt(self.delT) * Z))
        
        # Save the final simulated prices and their histories
        self.sim_results = S
        
    def _find_call_option_price(self):
        if self.sim_results is None:
            self.simulate_prices()
        # Get the current value of the mean of the option payoffs at maturity
        return np.exp(-self.r * self.T) * np.mean(np.maximum(self.sim_results[-1] - self.K, 0))
    
    def _find_put_option_price(self):
        if self.sim_results is None:
            self.simulate_prices()
        # Get the current value of the mean of the option payoffs at maturity
        return np.exp(-self.r * self.T) * np.mean(np.maximum(self.K - self.sim_results[-1], 0))

    def plot_simulation_results(self, num_sim=10):
        """
        Plots the simulated price paths of the underlying asset.
        """
        
        if self.sim_results is None:
            print("Simulation results are not available.")
            return
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.sim_results[:, 0:num_sim])
        plt.title('Simulated Price Paths of Underlying Asset')
        plt.axhline(self.K, c='k', xmin=0, xmax=self.num_steps, label='Strike Price')
        plt.xlim([0, self.num_steps])
        plt.ylabel('Simulated price movements')
        plt.xlabel('Days in future')
        plt.title(f'First {num_sim}/{self.N} simulations')
        plt.legend(loc='best')
        plt.show()

    def plot_combined(self, data, ticker, column_name):
        """
        Plots the simulated price paths of the underlying asset along with historical data.
        """
        if self.sim_results is None:
            print("Simulation results are not available.")
            return
        
        sim_vals = np.mean(self.sim_results[:, 0:100], axis=1)

        plt.figure(figsize=(10, 6))
        plt.plot(sim_vals, label='Simulated Price Path', c='blue')
        plt.plot(data[column_name].values[:self.num_steps], label=f'{ticker} {column_name}', c='orange')
        plt.title('Simulated Price Paths of Underlying Asset')
        plt.axhline(self.K, c='k', xmin=0, xmax=self.num_steps, label='Strike Price')
        plt.xlim([0, self.num_steps])
        plt.ylabel('Simulated price movements')
        plt.xlabel('Days in future')
        plt.title(f'First {1}/{self.N} simulations')
        plt.legend(loc='best')
        #plt.show()


    
