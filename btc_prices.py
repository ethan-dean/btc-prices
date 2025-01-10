import time
import requests
import os
from datetime import datetime

def get_day_count_since_first_day():
    # Calculate the number of days since the first day
    # first day = day of block time from genesis block
    # Bitcoin Genesis Block = January 3, 2009
    first_day = datetime(2009, 1, 3)
    current_day = datetime.now()
    delta = current_day - first_day
    return delta.days

# Dynamically rotate through keys
API_KEYS=[]
MOD_DAY = get_day_count_since_first_day() % len(API_KEYS)

# Set up your API key and endpoint
API_KEY = API_KEYS[MOD_DAY]
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
PARAMS = {
    'symbol': 'BTC',
    'convert': 'USD'
}
HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY
}

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Base directory for logs
BASE_LOG_PATH = os.path.join(BASE_DIR, 'data_logs')
os.makedirs(BASE_LOG_PATH, exist_ok=True)

# Error log directory
ERROR_LOG_PATH = os.path.join(BASE_DIR, 'error.log')

def log_error(message):
    # Append an error message to the error log
    with open(ERROR_LOG_PATH, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - ERROR - {message}\n")

def fetch_bitcoin_price():
    try:
        response = requests.get(URL, headers=HEADERS, params=PARAMS)
        data = response.json()
        # Extract the Bitcoin price in USD
        price = data['data']['BTC']['quote']['USD']['price']
        timestamp = int(time.time())  # Current time in seconds since epoch
        return price, timestamp
    except Exception as _e:
        return None, None

def log_price_to_file(price, timestamp, day_count):
    # Log file path within the day-specific folder
    log_file_path = os.path.join(BASE_LOG_PATH, 'day_' + str(day_count) + '.txt')
    # Append the data
    with open(log_file_path, 'a') as f:
        f.write(f"{timestamp} {price}\n")

def main():
    # Calculate the number of days since the first day
    day_count = get_day_count_since_first_day()
    # Fetch and log Bitcoin price
    price, timestamp = fetch_bitcoin_price()
    if price is not None and timestamp is not None:
        log_price_to_file(price, timestamp, day_count)
        print(f"Logged to day {day_count}: {timestamp},{price}")
    else:
        print("Failed to fetch price.")
        log_error("Failed to fetch price.")
    

if __name__ == "__main__":
    main()
