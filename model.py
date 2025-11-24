"""
Sock Price Prediction Model
Predicts crew sock prices based on temporal patterns
"""
import numpy as np
from datetime import datetime
import pandas as pd


class SockPriceModel:
    """Time-based predictive pricing model for crew socks"""
    
    def __init__(self):
        self.base_price = 6.00
        
    def predict_price(self, day_of_week, hour, month, special_events=None):
        """
        Predict sock price based on temporal features
        
        Args:
            day_of_week: 0=Monday, 6=Sunday
            hour: 0-23
            month: 1-12
            special_events: list of active special events
        
        Returns:
            dict with price, factors, and recommendations
        """
        price = self.base_price
        factors = []
        
        if special_events is None:
            special_events = []
        
        # Day of week patterns
        if day_of_week == 0:  # Monday morning restocking
            if 6 <= hour <= 10:
                price += 1.50
                factors.append("Monday morning rush (+$1.50)")
        elif day_of_week == 1:  # Tuesday afternoon lull
            if 13 <= hour <= 16:
                price -= 2.00
                factors.append("Tuesday afternoon lull (-$2.00)")
        elif day_of_week in [5, 6]:  # Weekend
            if 18 <= hour <= 22:
                price += 0.75
                factors.append("Weekend evening shopping (+$0.75)")
        
        # Time of day patterns
        if 9 <= hour <= 21:  # Peak shopping hours
            price += 0.50
            factors.append("Peak shopping hours (+$0.50)")
        elif 0 <= hour <= 6:  # Late night discount
            price -= 1.00
            factors.append("Late night discount (-$1.00)")
        
        # Seasonal patterns
        if month in [12, 1, 2]:  # Winter - cold feet season
            price += 1.00
            factors.append("Winter season (+$1.00)")
        elif month in [6, 7, 8]:  # Summer clearance
            price -= 0.75
            factors.append("Summer clearance (-$0.75)")
        
        # Special events
        if "back_to_school" in special_events and month == 9:
            price += 2.50
            factors.append("Back-to-school rush (+$2.50)")
        
        if "black_friday" in special_events and month == 11:
            price -= 3.50
            factors.append("Black Friday sale (-$3.50)")
        
        if "post_holiday" in special_events and month == 12 and 26 <= datetime.now().day <= 31:
            price -= 3.00
            factors.append("Post-holiday clearance (-$3.00)")
        
        if "sock_day" in special_events:  # December 4th - National Sock Day
            price += 1.25
            factors.append("National Sock Day premium (+$1.25)")
        
        # Ensure price doesn't go below reasonable minimum
        price = max(price, 2.50)
        
        return {
            "price": round(price, 2),
            "factors": factors,
            "base_price": self.base_price,
            "savings": round(self.base_price - price, 2) if price < self.base_price else 0
        }
    
    def get_weekly_prices(self, hour, month, special_events=None):
        """Get prices for entire week at specified hour"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        prices = []
        
        for day_idx in range(7):
            result = self.predict_price(day_idx, hour, month, special_events)
            prices.append({
                "day": days[day_idx],
                "price": result["price"],
                "day_idx": day_idx
            })
        
        return prices
    
    def get_daily_prices(self, day_of_week, month, special_events=None):
        """Get prices for 24 hours of a specific day"""
        prices = []
        
        for hour in range(24):
            result = self.predict_price(day_of_week, hour, month, special_events)
            prices.append({
                "hour": hour,
                "price": result["price"]
            })
        
        return prices
    
    def find_best_time(self, month, special_events=None):
        """Find the best day/time to buy socks"""
        best_price = float('inf')
        best_day = None
        best_hour = None
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for day_idx in range(7):
            for hour in range(24):
                result = self.predict_price(day_idx, hour, month, special_events)
                if result["price"] < best_price:
                    best_price = result["price"]
                    best_day = days[day_idx]
                    best_hour = hour
        
        return {
            "day": best_day,
            "hour": best_hour,
            "price": best_price
        }
