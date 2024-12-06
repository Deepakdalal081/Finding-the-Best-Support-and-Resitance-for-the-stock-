import mplfinance as mpf  # For candlestick plotting
import datetime as dt  # For handling date and time
import pandas_datareader.data as web  # For financial data fetching (not used here but included)
import matplotlib.pyplot as plt  # For general plotting (not used here but included)
import yfinance as yf  # For downloading stock data
import numpy as np  # For numerical operations
import pandas as pd  # For data manipulation

# Set the date range for data collection
end_date = dt.date.today()  # Today's date
start_date = end_date - dt.timedelta(days=100)  # Date 100 days before today

# List of stock symbols to analyze
stocks = ["TCS.NS"]  # Add more stock symbols as needed

for stock in stocks:
    # Download stock data for the given stock and date range
    data = yf.download(stock, start=start_date, end=end_date)  
    
    # Initialize lists to store support and resistance counts
    support_count = []
    resit_count = []
    
    # Iterate over each row in the data
    for i in range(len(data)):
        # Calculate the difference of the High column from the current row's High value
        high = data["High"][0:] - data["High"].iloc[i]
        
        # Define a limit (0.5% of the current High value) for resistance levels
        high_limit = np.round(((data["High"].iloc[i]) * (.005)), 2)
        
        # Identify points within the resistance range
        lenth = ((high > -high_limit) & (high < high_limit))
        
        # Count the number of True values, representing resistance occurrences
        resitance = lenth.sum()
        resit_count.append(resitance)
        
        # Calculate the difference of the Low column from the current row's Low value
        low = data["Low"][0:] - data["Low"].iloc[i]
        
        # Define a limit (0.5% of the current Low value) for support levels
        low_limit = np.round(((data["Low"].iloc[i]) * (.005)), 2)
        
        # Identify points within the support range
        lenth = ((low > -low_limit) & (low < low_limit))
        
        # Count the number of True values, representing support occurrences
        support = lenth.sum()
        support_count.append(support)
    
    # Add resistance counts as a new column in the DataFrame
    data["Resitance_points"] = resit_count
    
    # Sort the DataFrame by resistance points in descending order
    best_rest = data.sort_values(by="Resitance_points", ascending=False)
    
    # Add support counts as a new column in the DataFrame
    data["Support_points"] = support_count
    
    # Sort the DataFrame by support points in descending order
    best_supp = data.sort_values(by="Support_points", ascending=False)

# Extract the highest resistance point from the sorted DataFrame
best_resitance = best_rest["High"].head(1)

# Extract the highest support point from the sorted DataFrame
best_support = best_supp["Low"].head(1)

# Combine the best resistance and support points into a single series
levels = pd.concat([best_resitance, best_support])

# Plot the candlestick chart with horizontal lines for support and resistance
mpf.plot(
    data, 
    type="candle", 
    hlines=dict(hlines=levels.tolist(), colors=['r', 'g'], linewidths=0.7), 
    style="yahoo", 
    volume=True, 
    title="Support and Resistance", 
    figsize=(8, 4)
)
