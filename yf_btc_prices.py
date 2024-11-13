# import time
# import requests
import os
from datetime import datetime, timezone, timedelta
import yfinance as yf
import pandas as pd

# Set the number of days that the script pulls data for
NUM_DAYS_OF_DATA = 5

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Base directory for logs
BASE_LOG_PATH = os.path.join(BASE_DIR, 'yf_data_logs')
os.makedirs(BASE_LOG_PATH, exist_ok=True)

# Error log directory
ERROR_LOG_PATH = os.path.join(BASE_DIR, 'error.log')

def log_error(message):
    # Append an error message to the error log
    with open(ERROR_LOG_PATH, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} - ERROR - {message}\n')

def fetch_bitcoin_prices():
    try:
        # Set start and end dates to fetch full 5 days of historical data
        end_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=1)

        # Use yfinance to get Bitcoin's price data for 5 full days at 1-minute intervals
        ticker = yf.Ticker('BTC-USD')

        # 1-minute interval for NUM_DAYS_OF_DATA
        data = ticker.history(start=start_date, end=end_date, interval="1m")       # Use yfinance to get Bitcoin's price data for the entire day at 1-minute intervals
        # data = ticker.history(period=f'{NUM_DAYS_OF_DATA}d', interval="1m")

        # Extract the 'Close' column and reset the index to use the time as a column
        data = data[['Close']].reset_index()
        data.columns = ['time', 'price']

        # Debug to check number of rows
        original_num_rows = data.shape[0]
        print(f'API Data, Original Number of Rows: {original_num_rows}')

        # Ensure the last day has a price at 23:59
        last_day_end = end_date - timedelta(minutes=1)
        if data['time'].max() < last_day_end:
            # Append a row with the last available price if the 23:59 entry is missing
            last_price = data['price'].iloc[-1]
            data = pd.concat([data, pd.DataFrame({'time': [last_day_end], 'price': [last_price]})])       

        # Forward fill the data to fill in any minutes where data had no price 
        # likely due to low price volatility
        data = data.set_index('time').asfreq('1min').ffill().reset_index()

        # Debug to check the number of rows
        print(f'API Data, Filled Number of Rows: {data.shape[0]}')

        # Convert the 'time' column to seconds since epoch
        data['time'] = data['time'].astype('int64') // 10**9  # Convert datetime to Unix timestamp

        return data
    except Exception as _e:
        print(f'Error fetching prices: {_e}')
        return None

def log_price_to_file(data):
    # Ensure the 'time' column is integer and convert it to datetime for grouping
    data['time'] = data['time'].astype(int)
    data['date'] = pd.to_datetime(data['time'], unit='s').dt.date
    
    # Group by 'date' to separate data for each day
    for date, daily_data in data.groupby('date'):
        # Calculate the day count relative to the start date (2009-01-03)
        cur_day = pd.Timestamp(date).tz_localize('UTC')
        first_day = pd.Timestamp('2009-01-03', tz='UTC')
        day_count = (cur_day - first_day).days
        log_file_path = os.path.join(BASE_LOG_PATH, f'day_{day_count}.txt')
        
        # Write daily data to the file without the 'date' column
        daily_data[['time', 'price']].to_csv(log_file_path, sep=' ', header=False, index=False)

def main():
    # Fetch and log Bitcoin price
    data = fetch_bitcoin_prices()
    if data is not None:
        log_price_to_file(data)
        print(f'Logged: {data}')
    else:
        print('Failed to fetch price.')
        log_error('Failed to fetch price.')
    

if __name__ == '__main__':
    main()
