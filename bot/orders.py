from bot.client import BinanceFuturesClient
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.logging_config import setup_logger

logger = setup_logger()


def place_trade(symbol: str, side: str, order_type: str, quantity, price=None):
    """
    Validates input, then places an order via BinanceFuturesClient.
    Returns a dict with the order summary and response, or raises an exception on failure.
    """
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)

    order_summary = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "price": price if order_type == "LIMIT" else "N/A (MARKET)",
    }

    print("\n--- Order Request Summary ---")
    for key, value in order_summary.items():
        print(f"{key}: {value}")

    logger.info(f"Validated order request: {order_summary}")

    client = BinanceFuturesClient()

    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        print("\n--- Order Response ---")
        print(f"Order ID     : {response.get('orderId')}")
        print(f"Status       : {response.get('status')}")
        print(f"Executed Qty : {response.get('executedQty')}")
        print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
        print("\n✅ Order placed successfully.\n")

        return response

    except Exception as e:
        print(f"\n❌ Order failed: {e}\n")
        logger.error(f"Order placement failed: {e}")
        raise