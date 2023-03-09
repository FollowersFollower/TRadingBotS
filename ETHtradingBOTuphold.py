import ccxt
import time

# Set up the exchange object
exchange = ccxt.uphold({
    'apiKey': 'your_api_key',
    'secret': 'your_secret_key'
})

# Set up the trading parameters
symbol = 'ETH/USD'
amount = 1  # The amount of ETH to buy/sell
profit_margin = 0.02  # The desired profit margin

# The main trading loop
while True:
    # Fetch the latest market data
    ticker = exchange.fetch_ticker(symbol)
    bid, ask = ticker['bid'], ticker['ask']

    # Calculate the target buy and sell prices
    buy_price = bid
    sell_price = bid * (1 + profit_margin)

    # Check the account balance
    eth_balance = exchange.fetch_balance()['ETH']['free']
    usd_balance = exchange.fetch_balance()['USD']['free']

    # Place a buy order if the conditions are met
    if eth_balance >= amount and usd_balance >= buy_price * amount:
        print('Placing buy order...')
        order = exchange.create_limit_buy_order(symbol, amount, buy_price)
        print(order)
    
    # Place a sell order if the conditions are met
    elif eth_balance >= amount and ticker['high'] >= sell_price:
        print('Placing sell order...')
        order = exchange.create_limit_sell_order(symbol, amount, sell_price)
        print(order)
    
    # Wait for the next iteration
    time.sleep(60)

import ccxt

exchange = ccxt.uphold({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'enableRateLimit': True,
})

symbol = 'ETH/USD'
amount = 0.01

# Check if the symbol is valid and trading is allowed
if symbol in exchange.load_markets() and exchange.markets[symbol]['trading']:
    # Check if the amount is within the minimum and maximum order limits
    amount_info = exchange.fetch_ticker(symbol)['info']['pairs'][symbol]['minOrderAmount']
    if amount_info['currency'] == 'USD':
        min_amount = amount_info['amount']
    else:
        min_amount = amount_info['amount'] * exchange.fetch_ticker(symbol)['last']
    max_amount = exchange.calculate_max_amount(symbol, 1000, 'limit', 'buy')
    if min_amount <= amount <= max_amount:
        # Place the order
        order = exchange.create_order(symbol, 'limit', 'buy', amount, None, {'price': exchange.fetch_ticker(symbol)['ask']})
        print(order)
    else:
        print(f"Amount must be between {min_amount:.2f} and {max_amount:.2f} {symbol.split('/')[1]}")
else:
    print(f"{symbol} is not available for trading on {exchange.name}")
