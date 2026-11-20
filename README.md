# Wi-Fi Speed Checker

A small, browser-based internet speed checker powered by Python. Run it locally, open the page in your browser, and check your download speed, upload speed, and ping.

## Features

- One-click speed test
- Download and upload speeds shown in Mbps
- Ping shown in milliseconds
- Lightweight HTML, CSS, and JavaScript interface
- Local Python server; the app is not hosted online


## Screenshots
<img width="1637" height="911" alt="screenshot main" src="https://github.com/user-attachments/assets/f05dc8da-a0c7-4760-ab5f-6ca37db3266e" />

<img width="1636" height="911" alt="screenshot 1" src="https://github.com/user-attachments/assets/1ccc7c9f-707a-4917-bcdf-9ff7434b7c34" />


## Requirements

- Python 3
- An internet connection

## Run locally

Clone the repository and move into its folder (replace `YOUR-USERNAME` with your GitHub username):

```bash
git clone https://github.com/YOUR-USERNAME/wifi-speed-checker.git
cd wifi-speed-checker
```

Create a virtual environment and install the dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the app:

```bash
./run.sh
```

The app should open in your browser at <http://127.0.0.1:8765>. Keep the Terminal window open while using it; press **Ctrl+C** there to stop the server.

If the launcher does not run, start the app directly:

```bash
./.venv/bin/python main.py
```

## Notes

The speed test needs an internet connection and may use a significant amount of data. Results can vary based on your network, device, and selected test server.
