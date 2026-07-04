import argparse
import sys
from bot.orders import place_trade
from bot.logging_config import setup_logger

logger = setup_logger()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simplified Trading Bot - Binance Futures Testnet"
    )

    parser.add_argument(
        "--symbol", required=True, help="Trading pair symbol, e.g., BTCUSDT"
    )
    parser.add_argument(
        "--side", required=True, choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "--type", required=True, dest="order_type",
        choices=["MARKET", "LIMIT", "STOP", "market", "limit", "stop"],
        help="Order type: MARKET, LIMIT, or STOP"
    )
    parser.add_argument(
        "--quantity", required=True, type=float, help="Order quantity"
    )
    parser.add_argument(
        "--price", required=False, type=float, default=None,
        help="Order price (required for LIMIT and STOP orders)"
    )
    parser.add_argument(
        "--stop-price", required=False, type=float, default=None, dest="stop_price",
        help="Stop trigger price (required only for STOP orders)"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    logger.info(f"CLI invoked with args: {vars(args)}")

    try:
        place_trade(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except Exception as e:
        logger.error(f"CLI execution failed: {e}")
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()