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
ExecStart=/usr/bin/python3 /path/to/bitcoin_price_logger.py
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
OnCalendar=*:0/1
Persistent=true

[Install]
WantedBy=timers.target
```

OnCalendar=*:0/1: Runs the timer every minute.
Persistent=true: Ensures that missed runs (e.g., if the system is off) are made up for on the next activation.

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
```

### Step 4: Check the Status
To verify that the timer is running:
```bash
systemctl status bitcoin_price_logger.timer
```

To check logs for the script’s output:
```bash
journalctl -u bitcoin_price_logger.service -f
```


Summary
This setup ensures the script runs once per minute, logging the Bitcoin price without requiring a continuous loop inside the script. The timer triggers the bitcoin_price_logger.service every minute, effectively running the script as a scheduled task.referred setup is 
