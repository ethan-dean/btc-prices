import time
import requests
import os
from datetime import datetime, timedelta

# Set up your API key and endpoint
API_KEY = 'API_KEY'
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
BASE_LOG_PATH = os.path.join(BASE_DIR, 'bitcoin_logs')
os.makedirs(BASE_LOG_PATH, exist_ok=True)

# Error log directory
ERROR_LOG_PATH = os.path.join(BASE_DIR, 'error.log')

# First day file to store the initial timestamp
FIRST_DAY_FILE = os.path.join(BASE_LOG_PATH, 'first_day.txt')

def log_error(message):
    # Append an error message to the error log
    with open(ERROR_LOG_PATH, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - ERROR - {message}\n")

def get_first_block_timestamp():
    # Return block time of bitcoin genesis block
    return datetime.fromtimestamp(1231006505)

def get_day_count_since_first_day(first_day_timestamp):
    # Calculate the number of days since the first day
    first_day = first_day_timestamp
    current_day = datetime.now()
    delta = current_day - first_day
    return delta.days

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
    log_file_path = os.path.join(BASE_LOG_PATH, str(day_count) + '.txt')
    
    # Append the data
    with open(log_file_path, 'a') as f:
        f.write(f"{timestamp} {price}\n")

def main():
    # Get the first day timestamp
    first_day_timestamp = get_first_block_timestamp()
    
    # Calculate the number of days since the first day
    day_count = get_day_count_since_first_day(first_day_timestamp)
    
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
