from bot.client import BinanceFuturesClient
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_stop_price,
)
from bot.logging_config import setup_logger

logger = setup_logger()


def place_trade(symbol: str, side: str, order_type: str, quantity, price=None, stop_price=None):
    """
    Validates input, then places an order via BinanceFuturesClient.
    Returns a dict with the order summary and response, or raises an exception on failure.
    """
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)
    stop_price = validate_stop_price(stop_price, order_type)

    order_summary = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "price": price if order_type in ("LIMIT", "STOP") else "N/A (MARKET)",
        "stop_price": stop_price if order_type == "STOP" else "N/A",
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
            stop_price=stop_price,
        )
        print("\n--- Order Response ---")
        order_id = response.get('orderId') or response.get('algoId')
        status = response.get('status') or response.get('algoStatus')
        print(f"Order ID     : {order_id}")
        print(f"Status       : {status}")
        print(f"Executed Qty : {response.get('executedQty', 'N/A')}")
        print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
        if order_type == "STOP":
            print(f"Trigger Price: {response.get('triggerPrice', 'N/A')}")
        print("\n✅ Order placed successfully.\n")
        return response

    except Exception as e:
        print(f"\n❌ Order failed: {e}\n")
        logger.error(f"Order placement failed: {e}")
        raise