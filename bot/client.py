import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from bot.logging_config import setup_logger

load_dotenv()

logger = setup_logger()

class BinanceFuturesClient:
    """
    Wrapper around the python-binance Client, configured for Futures Testnet.
    """

    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            logger.error("API key/secret not found in .env file")
            raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in .env")

        try:
            self.client = Client(api_key, api_secret)

            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
            logger.info("Binance Futures Testnet client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
        """
        Places an order on Binance Futures Testnet.
        Returns the raw API response as a dict.
        """
        order_params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            order_params["price"] = price
            order_params["timeInForce"] = "GTC"  # Good 'Til Cancelled

        elif order_type == "STOP":
            order_params["price"] = price
            order_params["stopPrice"] = stop_price
            order_params["timeInForce"] = "GTC"

        logger.info(f"Sending order request: {order_params}")

        try:
            response = self.client.futures_create_order(**order_params)
            logger.info(f"Order response received: {response}")
            return response
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise
        except BinanceOrderException as e:
            logger.error(f"Binance order error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while placing order: {e}")
            raise
