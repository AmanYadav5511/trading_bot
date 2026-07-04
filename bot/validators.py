from bot.logging_config import setup_logger

logger = setup_logger()

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    """
    Basic check that symbol looks like a valid trading pair (e.g., BTCUSDT).
    """
    if not symbol:
        logger.error("Symbol is empty")
        raise ValueError("Symbol cannot be empty")

    symbol = symbol.upper().strip()

    if not symbol.isalnum():
        logger.error(f"Invalid symbol format: {symbol}")
        raise ValueError(f"Symbol must be alphanumeric (e.g., BTCUSDT). Got: {symbol}")

    if len(symbol) < 5:
        logger.error(f"Symbol too short: {symbol}")
        raise ValueError(f"Symbol looks too short to be valid: {symbol}")

    return symbol


def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in VALID_SIDES:
        logger.error(f"Invalid side: {side}")
        raise ValueError(f"Side must be one of {VALID_SIDES}. Got: {side}")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        logger.error(f"Invalid order type: {order_type}")
        raise ValueError(f"Order type must be one of {VALID_ORDER_TYPES}. Got: {order_type}")
    return order_type


def validate_quantity(quantity) -> float:
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        logger.error(f"Quantity is not a valid number: {quantity}")
        raise ValueError(f"Quantity must be a number. Got: {quantity}")

    if quantity <= 0:
        logger.error(f"Quantity must be positive: {quantity}")
        raise ValueError(f"Quantity must be greater than 0. Got: {quantity}")

    return quantity


def validate_price(price, order_type: str):
    """
    Price is required only for LIMIT orders.
    """
    if order_type == "LIMIT":
        if price is None:
            logger.error("Price is required for LIMIT orders but was not provided")
            raise ValueError("Price is required for LIMIT orders")
        try:
            price = float(price)
        except (TypeError, ValueError):
            logger.error(f"Price is not a valid number: {price}")
            raise ValueError(f"Price must be a number. Got: {price}")

        if price <= 0:
            logger.error(f"Price must be positive: {price}")
            raise ValueError(f"Price must be greater than 0. Got: {price}")

        return price

    return None  # MARKET orders don't need a price