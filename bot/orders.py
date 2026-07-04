import time
from bot.client import BinanceFuturesClient
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


def print_divider():
    print("=" * 45)


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
        "Symbol": symbol,
        "Side": side,
        "Type": order_type,
        "Quantity": quantity,
        "Price": price if order_type in ("LIMIT", "STOP") else "N/A (MARKET)",
        "Stop Price": stop_price if order_type == "STOP" else "N/A",
    }

    print_divider()
    print("ORDER REQUEST")
    print_divider()
    for key, value in order_summary.items():
        print(f"{key:<12}: {value}")

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

        order_id = response.get('orderId') or response.get('algoId')
        status = response.get('status') or response.get('algoStatus')
        executed_qty = response.get('executedQty', 'N/A')
        avg_price = response.get('avgPrice', 'N/A')

        # For MARKET/LIMIT orders, briefly wait and re-fetch to get actual fill details
        if order_type in ("MARKET", "LIMIT") and order_id:
            time.sleep(1)
            updated = client.get_order_status(symbol, order_id)
            if updated:
                status = updated.get('status', status)
                executed_qty = updated.get('executedQty', executed_qty)
                avg_price = updated.get('avgPrice', avg_price)

        print()
        print_divider()
        print("ORDER RESPONSE")
        print_divider()
        print(f"{'Order ID':<12}: {order_id}")
        print(f"{'Status':<12}: {status}")
        print(f"{'Executed Qty':<12}: {executed_qty}")
        print(f"{'Avg Price':<12}: {avg_price}")
        if order_type == "STOP":
            print(f"{'Trigger':<12}: {response.get('triggerPrice', 'N/A')}")
        print_divider()
        print("SUCCESS: Order placed successfully")
        print_divider()
        print()

        return response

    except Exception as e:
        print()
        print_divider()
        print("FAILED: Order could not be placed")
        print(f"Reason: {e}")
        print_divider()
        print()
        logger.error(f"Order placement failed: {e}")
        raise