# Bitcoin Prices
Collection of minutewise prices from API for backtesting.
Current API in use is CoinMarketCap Basic tier.

## Setup
### Step 1: Create the systemd Service File
Save your Python script as /path/to/bitcoin_price_logger.py and make it executable:
```bash
chmod +x /path/to/bitcoin_price_logger.py
```

Create a systemd service file. Open a new file:
```bash
sudo nano /etc/systemd/system/bitcoin_price_logger.service
```

Add the following configuration to the file(UPDATE THE PATH):
```ini
[Unit]
Description=Bitcoin Price Logger Service

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /path/to/btc_prices.py
```

Save and close the file.

Save your Python script as /path/to/yf_bitcoin_price_logger.py and make it executable:
```bash
chmod +x /path/to/yf_bitcoin_price_logger.py
```

Create a systemd service file. Open a new file:
```bash
sudo nano /etc/systemd/system/yf_bitcoin_price_logger.service
```

Add the following configuration for using the yfinance script:
```ini
[Unit]
Description=yf Bitcoin Price Logger Service

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /path/to/yf_btc_prices.py
```

Type=oneshot: Ensures the service only runs once per invocation.
ExecStart: Specifies the command to execute the script.

Save and close the file.

### Step 2: Create the systemd Timer File
Create a new timer file:
```bash
sudo nano /etc/systemd/system/bitcoin_price_logger.timer
```

Add the following configuration to the file:
```ini
[Unit]
Description=Run Bitcoin Price Logger every minute

[Timer]
OnCalendar=*-*-* *:*:00
AccuracySec=1s

[Install]
WantedBy=timers.target
```

OnCalendar=*:*:* *:*:00 runs the timer once a minute on the 0th second.

Save and close the file.

Create a new timer file:
```bash
sudo nano /etc/systemd/system/yf_bitcoin_price_logger.timer
```

Add the following configuration for using the yfinance script:
```ini
[Unit]
Description=Run yf Bitcoin Price Logger once a day

[Timer]
OnCalendar=*-*-* 00:00:30
AccuracySec=1s

[Install]
WantedBy=timers.target
```

OnCalendar=*:*:* 00:00:30 runs the timer once a day at 12:00:30am.

Save and close the file.

### Step 3: Enable and Start the Timer
Reload systemd to recognize the new files:
```bash
sudo systemctl daemon-reload
```

Enable and start the timer to begin running the script every minute:
```bash
sudo systemctl enable bitcoin_price_logger.timer
sudo systemctl start bitcoin_price_logger.timer
sudo systemctl enable yf_bitcoin_price_logger.timer
sudo systemctl start yf_bitcoin_price_logger.timer
```

### Step 4: Check the Status
To verify that the timer is running:
```bash
systemctl status bitcoin_price_logger.timer
```
or
```bash
systemctl status yf_bitcoin_price_logger.timer
```

To check logs for the script’s output:
```bash
journalctl -u bitcoin_price_logger.service -f
```
or
```bash
journalctl -u yf_bitcoin_price_logger.service -f
```

### NOTE: yfinance Sourcing Package Managers
If using a package manager that needs to be sourced to access the yfinance package ensure the yf_bitcoin_price_logger.service ExecStart is adjusted.

For example for Miniconda:
```ini
[Unit]
Description=yf Bitcoin Price Logger Service

[Service]
Type=oneshot
ExecStart=/bin/bash -c "source /path/to/miniconda3/bin/activate && conda activate your_env && python /path/to/btc_prices/yf_btc_prices.py"
```
