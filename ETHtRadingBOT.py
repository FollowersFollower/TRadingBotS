import time
import ccxt

# Exchange API keys
exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'enableRateLimit': True
})

# Trading parameters
symbol = 'ETH/USDT'
amount = 0.1
take_profit = 1.05
stop_loss = 0.95

# Run trading bot
while True:
    try:
        # Get current market price
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']

        # Check if position is open
        positions = exchange.private_get_positionrisk({'filter': json.dumps({'symbol': symbol})})
        position_size = float(positions[0]['positionAmt'])
        if position_size == 0:
            # Place new buy order
            buy_order = exchange.create_order(symbol, 'limit', 'buy', amount, current_price)
            buy_price = buy_order['price']
            take_profit_price = buy_price * take_profit
            stop_loss_price = buy_price * stop_loss
            print('Bought {} ETH at price {}'.format(amount, buy_price))
        else:
            # Check if take profit or stop loss has been hit
            if current_price >= take_profit_price or current_price <= stop_loss_price:
                # Close position
                side = 'sell' if position_size > 0 else 'buy'
                exchange.create_order(symbol, 'limit', side, abs(position_size), current_price)
                print('Sold {} ETH at price {}'.format(abs(position_size), current_price))
            else:
                print('Current price: {}'.format(current_price))

        # Wait for 5 seconds before checking price again
        time.sleep(5)
        
    except Exception as e:
        print('Error: {}'.format(str(e)))



json = {
    "exchange": "binance",
    "symbol": "ETH/USDT",
    "order_type": "market",
    "side": "buy",
    "quantity": "0.1"
}
