# To make a basic framework for any of the option pricing models
# Essentially, accept the same inputs and provide a common interface for calculating option prices

from abc import ABC, abstractmethod

class OptionModel(ABC):
    # Basic framework for option pricing models
    def calculate_option_price(self, option_type):

        option_type = option_type.lower()
        option_price = -1

        # Check the option type and call the appropriate method to calculate the price
        if (option_type == 'call'):
            # print("Calculating Call Option Price...")
            option_price = self._find_call_option_price()
        elif (option_type == 'put'):
            # print("Calculating Put Option Price...")
            option_price = self._find_put_option_price()
        else:
            print("Option type must be Call or Put ! Invalid option type provided.")
        return option_price
    
    # Defining the abstract methods for finding call and put option prices
    # These methods will be implemented in the derived classes
    @classmethod
    @abstractmethod
    def _find_call_option_price(cls):
        # Abstract method to find call option price
        pass

    @classmethod
    @abstractmethod
    def _find_put_option_price(cls):
        # Abstract method to find put option price
        pass