# import binance
#
#
# def place_order(action, symbol, quantity, price):
#     if action == "buy":
#         order_type = binance.OrderType.LIMIT_BUY
#     elif action == "sell":
#         order_type = binance.OrderType.LIMIT_SELL
#     else:
#         raise ValueError("Invalid action")
#
#     client = binance.Client()
#     order = client.create_order(
#         symbol=symbol,
#         side=action,
#         quantity=quantity,
#         price=price,
#         order_type=order_type
#     )
#
#     print(f"Order placed: {order}")
#
# def main():
#     symbol = "USDTNGN"
#     action = input("Enter action (buy/sell): ")
#     profit_margin = float(input("Enter profit margin: "))
#     quantity = 1
#
#     current_price = get_current_price(symbol)
#
#     place_order(action, symbol, quantity, current_price)
#
#     while True:
#         new_price = get_current_price(symbol)
#
#         if action == "buy" and new_price >= current_price + profit_margin:
#             print("Profit target reached, selling...")
#             place_order("sell", symbol, quantity, new_price)
#             break
#         elif action == "sell" and new_price <= current_price - profit_margin:
#             print("Stop loss reached, buying...")
#             place_order("buy", symbol, quantity, new_price)
#             break
#
#
# def get_current_price(symbol):
#     client = binance.Client()
#     ticker = client.get_ticker(symbol)
#     return ticker["price"]
#
#
# if __name__ == "__main__":
#     main()


import time
from binance.client import Client

# Binance API credentials
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

# User inputs
action = input("Enter 'buy' or 'sell' action: ")
profit_margin = float(input("Enter the profit margin: "))


# Function to place a spot limit order
def place_limit_order(symbol, side, quantity, price):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=Client.ORDER_TYPE_LIMIT,
            timeInForce=Client.TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=str(price)
        )
        print(f"Limit order placed: {order}")
        return True
    except Exception as e:
        print(f"Error placing limit order: {e}")
        return False


# Function to check current price
def get_current_price(symbol):
    try:
        ticker = client.get_ticker(symbol=symbol)
        return float(ticker['lastPrice'])
    except Exception as e:
        print(f"Error retrieving current price: {e}")
        return None


# Main script
if action == 'buy':
    symbol = 'USDTNGN'
    quantity = 10  # Example quantity, you can change this as per your requirement
    current_price = get_current_price(symbol)

    if current_price is not None:
        target_price = current_price + profit_margin

        if place_limit_order(symbol, Client.SIDE_BUY, quantity, current_price):
            print(f"Waiting for the price to reach {target_price} for the sell action...")

            while True:
                current_price = get_current_price(symbol)

                if current_price >= target_price:
                    if place_limit_order(symbol, Client.SIDE_SELL, quantity, current_price):
                        print("Second action executed. Exiting the script.")
                        break

                time.sleep(10)  # Adjust the time interval as per your requirement
else:
    print("Invalid action. Please enter 'buy' or 'sell'.")
