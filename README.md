# Trading Bot - Binance Futures Testnet

A simplified Python CLI application to place market orders and limit orders on BINANCE FUTURES TESTNET (USDT-M), built with a clean, modular structure and proper logging/error handling.

## Project Structure

trading_bot/
├── bot/
│   ├── init.py
│   ├── client.py              # Binance client wrapper (API layer)
│   ├── orders.py              # Order placement logic
│   ├── validators.py          # Input validation
│   └── logging_config.py      # Logging setup
├── cli.py                     # CLI entry point
├── requirements.txt
├── .env                       # API credentials not committed
└── README.md


## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/trading_bot.git
cd trading_bot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Binance Futures Testnet API credentials

1. Register at [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Generate an API Key and Secret from the testnet dashboard
3. Create a `.env` file in the project root:



## How to Run

### Place a MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
```

### CLI Arguments

| Argument | Required | Description |
|---|---|---|
| `--symbol` | Yes | Trading pair, e.g., `BTCUSDT` |
| `--side` | Yes | `BUY` or `SELL` |
| `--type` | Yes | `MARKET` or `LIMIT` |
| `--quantity` | Yes | Order quantity (positive number) |
| `--price` | Only for LIMIT | Order price (positive number) |

## Logging

All API requests, responses, and errors are logged to `trading_bot.log` in the project root, with timestamps and log levels. Logs are also printed to the console for real-time feedback.

## Error Handling

- Invalid CLI input (bad symbol, side, order type, quantity, or missing price for LIMIT orders) is caught and reported clearly before any API call is made.
- Binance API errors (e.g., invalid symbol, insufficient balance) are caught, logged, and displayed with a clear failure message.
- Network/connection failures are caught and logged without crashing the application.

## Assumptions

- This application is configured exclusively for **Binance Futures Testnet** (`https://testnet.binancefuture.com`) and is not intended for live trading.
- Quantity is assumed to be in the base asset unit (e.g., BTC for BTCUSDT).
- Only `MARKET` and `LIMIT` order types are supported as core functionality (per assignment requirements).
- `GTC` (Good-Til-Cancelled) is used as the default `timeInForce` for LIMIT orders.

## Tech Stack

- Python 3.x
- [python-binance](https://github.com/sammchardy/python-binance)
- python-dotenv



