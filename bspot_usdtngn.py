'''
    OK
    --- jbadonaiventures ---
    IT'S ALL ABOUT SELLING OR BUYNG USDT WITH NGN
    SELL USDT GET NGN
    BUY USDT WITH NGN
'''

try:
    from decimal import Decimal
    from binance.enums import *
    from binance.client import Client
    import time
    from binance.exceptions import BinanceAPIException
    import os

    def clear_screen():
        if os.name == 'posix':
            # For Unix-like systems (e.g. Linux, macOS)
            os.system('clear')
        elif os.name == 'nt':
            # For Windows
            os.system('cls')

    # initialize Binance client

    # while True:
    #     clear_screen()
    #     access_code = input("Access Code? ")
    #     if access_code == "jesusislord":
    #         break

    api_key = input("Binance API key:")
    api_secret = input("Binance Secret key: ")
    clear_screen()
    client = Client(api_key, api_secret)

    # start trading loop
    symbol = "USDTNGN"
    auto_mid_price = False
    auto_stake_amount = False

    def convert_seconds(seconds):
        days = seconds // (24 * 3600)
        seconds %= 24 * 3600
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return f"{days}d:{hours}h:{minutes}m:{seconds}s"


    def get_balance(client, asset):
        balances = client.get_account()['balances']
        for balance in balances:
            if balance['asset'] == asset:
                return float(balance['free'])
        return 0


    def get_highest_lowest_prices():
        global symbol
        # get the 24-hour ticker for symbol
        ticker = client.get_ticker(symbol=symbol)

        # extract the highest and lowest prices
        highest_price = Decimal(ticker['highPrice'])
        lowest_price = Decimal(ticker['lowPrice'])

        return highest_price, lowest_price

    def auto_calculate_mid_price():
        hlp = get_highest_lowest_prices()
        lowest = hlp[1]
        highest = hlp[0]
        mid_value = (lowest + highest) / 2

        print(lowest, highest, mid_value)
        return mid_value

    def show_trading_stat():
        global  mid_price, profit_margin, current_order,stake_dollar_amount, sell_Dollar_price, \
            buy_Dollar_price, stake_dollar_percent, symbol
        print()
        print("**********************************************************")
        print("TRADING STATISTICS")
        print("**********************************************************")
        print(f"[*] - Symbol: {symbol}")
        print(f"[*] - Staked dollar percentage: {stake_dollar_percent}")
        print(f"[*] - mid price: {mid_price}")
        # print(f"[*] - Actual profit margin: N{float(profit_margin) * 2}")
        print(f"[*] - current order: {current_order}")
        print(f"[*] - staked dollar amount: {stake_dollar_amount}")
        print(f"[*] - Sell Dollar price: {sell_Dollar_price}")
        print(f"[*] - Buy Dollar price: {buy_Dollar_price}")
        print("**********************************************************")
        print()

    profit_margin = profit_margin_default = 1
    mid_price = mid_price_default = 739.5
    sell_Dollar_price = mid_price + profit_margin   # sell USDT at high price
    buy_Dollar_price = mid_price - profit_margin    # buy USDT at low price
    current_order = 'buy'  # Starting with a buy order
    RECV_WINDOW = 5000  # in milliseconds
    stake_dollar_amount = stake_dollar_amount_default = 10
    total_completed_trade_cycle = 0
    sell_buy_quantity = 1
    stake_dollar_percent_default = stake_dollar_percent = 80


    def change_settings():
        global symbol, stake_dollar_percent, mid_price, profit_margin, current_order, \
            stake_dollar_amount, sell_Dollar_price, buy_Dollar_price

        smb = input("set symbol [ USDTNGN ] :  ")
        if smb == "":
            symbol = "USDTNGN"
        else:
            symbol = smb

        sdp = input("Set stake dollar percentage - [80]: ")
        if sdp == "":
            stake_dollar_percent = stake_dollar_percent_default
        else:
            stake_dollar_percent = int(sdp)

        mid_price = input("Set mid price - [739.5]/auto: ")
        if mid_price == "auto":
            auto_mid_price = True
            mid_price = auto_calculate_mid_price()
            mid_price = float(mid_price)
        elif mid_price == "":
            mid_price = mid_price_default
        else:
            mid_price = float(mid_price)

        profit_margin = input("Profit Margin - [1]:  ")
        if profit_margin == "":
            profit_margin = float(profit_margin_default)
        else:
            profit_margin = float(profit_margin)

        while True:
            current_order = input("Starting Order (buy/sell): ")
            if current_order == 'buy' or current_order == 'sell':
                break
            else:
                print("\t[?] - 'buy' or 'sell' response required! Try Again")

        stake_dollar_amount = input("stake dollar amount (10)/auto: ")
        if stake_dollar_amount == "":
            stake_dollar_amount = stake_dollar_amount_default
        elif stake_dollar_amount == 'auto':
            # get a percentage of the total balance and set it as the amount
            # include percentage as a settings which user can change
            auto_stake_amount = True
            usd_bal = get_balance(client, 'USDT')

            stake_dollar_amount = round((stake_dollar_percent/100) * usd_bal)
            print(f'usdt balance: {usd_bal}')
            print(f'staked dollar ammount: {stake_dollar_amount}')

            pass
        else:
            stake_dollar_amount = int(stake_dollar_amount)

        sell_Dollar_price = mid_price + profit_margin  # sell USDT at high price
        buy_Dollar_price = mid_price - profit_margin  # buy USDT at low price


    change_setting = input("Change Settings? y/n: ")
    if change_setting == 'y':
        change_settings()


    sell_Dollar_price = round(sell_Dollar_price,1)
    buy_Dollar_price = round(buy_Dollar_price,1)


    def get_symbol_ticker(client, symbol):
        return client.get_symbol_ticker(symbol=symbol)


    def place_buy_order(client, symbol, quantity, price):
        try:
            order = client.create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price)
            # print(f"Buy order placed:")
            return order
        except BinanceAPIException as e:
            print(f"Error placing buy order: {e}")
            return None


    def place_sell_order(client, symbol, quantity, price):
        try:
            # print(f"symbol: {symbol}")
            # print(f"quantity: {quantity}")
            # print(f"price: {price}")
            order = client.create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price)
            # print(f"Sell order placed: ")
            return order
        except BinanceAPIException as e:
            print(f"Error placing sell order: {e}")
            return None


    def format_float(value):
        """Formats the given value as a string with 8 decimal places."""

        return "{:.8f}".format(value)


    def format_float_3(value):
        """Formats the given value as a string with 8 decimal places."""
        return "{:.3f}".format(value)


    def place_buy_order_new(client, symbol, quantity, price):
        """Place a limit buy order for the given symbol, quantity and price."""
        symbol_info = client.get_symbol_info(symbol)
        # Get the LOT_SIZE filter information
        lot_size_filter = next(f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE')
        # Calculate the maximum quantity we can buy based on the LOT_SIZE filter
        step_size = float(lot_size_filter['stepSize'])
        max_qty = float(lot_size_filter['maxQty'])
        quantity = min(quantity, max_qty)
        quantity = quantity - quantity % step_size
        # print(f'initial quantity: {quantity}')
        # print(f"step size: {step_size}")
        # print(f"max qty: {max_qty}")
        # print(f"quantity: {quantity}")
        # print(f"price:  {format_float(price)}")
        # Place the buy order
        try:
            order = client.create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=format_float(price),
                recvWindow=RECV_WINDOW
            )
            print(f"Buy order placed: {order}")
            return order
        except BinanceAPIException as e:
            print(f"Error placing buy order: {e}")
            return None


    def place_sell_order_new(client, symbol, quantity, price):
        """Places a sell order on Binance"""
        try:
            symbol_info = client.get_symbol_info(symbol)

            step_size = symbol_info(client, symbol)['filters'][2]['stepSize']
            quantity = float(Decimal(quantity).quantize(Decimal(step_size)))
            order = client.create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price)
            print(f"Sell order placed: {order}")
            return order
        except BinanceAPIException as e:
            print(f"Error placing sell order: {e}")
            return None


    def get_symbol_info():
        global symbol, client
        # Get symbol info for a currency pair
        symbol_info = client.get_symbol_info(symbol)

        # Extract base and quote currencies from symbol info
        base_currency = symbol_info['baseAsset']
        quote_currency = symbol_info['quoteAsset']

        return base_currency, quote_currency


    def start_trading_loop_bak(client, symbol):
        global current_order
        counter = 0
        while True:
            # get current ticker price
            ticker_price = float(get_symbol_ticker(client, symbol)['price'])

            # buy order logic
            if get_balance(client, 'USDT') > 10 and current_order == 'buy':
                print(f"balance: {get_balance(client, 'USDT') }")
                # buy_quantity = round(10 / buy_Dollar_price, 8)
                buy_quantity = 1
                buy_order = place_buy_order(client, symbol, buy_quantity, buy_Dollar_price)
                if buy_order is not None:
                    current_order = 'sell'
                    counter = 0
                    while True:
                        counter += 1
                        print(f"Waiting for buy order to be filled...[ {counter} ]")
                        time.sleep(1)
                        order_status = client.get_order(symbol=symbol, orderId=buy_order['orderId'])
                        if order_status['status'] == 'FILLED':
                            break
                    print("Buy order filled")

            # sell order logic
            ngn_balance = get_balance(client, 'NGN')
            if ngn_balance > 0 and current_order == 'sell':
                sell_order = place_sell_order(client, symbol, ngn_balance, sell_Dollar_price)
                if sell_order is not None:
                    current_order = 'buy'
                    counter = 0
                    while True:
                        counter += 1
                        print(f"Waiting for sell order to be filled...[ {counter} ]")
                        time.sleep(1)
                        order_status = client.get_order(symbol=symbol, orderId=sell_order['orderId'])
                        if order_status['status'] == 'FILLED':
                            break
                    print("Sell order filled")

            # wait for a minute before checking again
            print(f"An Order is successfully executed. colling down to take the next order")
            time.sleep(60)


    def start_trading_loop(client):
        global current_order, total_completed_trade_cycle, buy_Dollar_price, \
            stake_dollar_amount, sell_Dollar_price, profit_margin, stake_dollar_percent, symbol

        counter = 0
        while True:
            clear_screen()
            print("=-=-=-=-=-=---=-=-=-=-=-=-=-=-=-=-=-=-===-=-=-=-=-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print(f"TOTAL COMPLETED TRADE CYCLE: {total_completed_trade_cycle}")
            show_trading_stat()
            print("=-=-=-=-=-=---=-=-=-=-=-=-=-=-=-=-=-=-===-=-=-=-=-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            # get current ticker price
            ticker_price = float(get_symbol_ticker(client, symbol)['price'])

            # separate currency into base and quote symbol
            base_currency, quote_currency = get_symbol_info()

            # sell order logic
            if get_balance(client, base_currency) > int(stake_dollar_amount) and current_order == 'sell':
                sell_quantity = int(stake_dollar_amount)
                sell_order = place_sell_order(client, symbol, sell_quantity, sell_Dollar_price)
                if sell_order is not None:
                    current_order = 'buy'
                    counter = 0
                    error_counter = 0
                    while True:
                        try:
                            counter += 1

                            ticker = client.get_ticker(symbol=symbol)
                            lp = Decimal(ticker['lastPrice'])

                            print(f"\r> Waiting for sell order to be filled...[{lp}]->[{sell_Dollar_price}] | [ {convert_seconds(counter)} ] | Error count = [{error_counter}]", end="")
                            time.sleep(1)
                            order_status = client.get_order(symbol=symbol, orderId=sell_order['orderId'])
                            if order_status['status'] == 'FILLED':
                                break
                        except Exception as e:
                            error_counter += 1
                            # print(f"\r> Waiting for sell order to be filled...[ {counter} ]\n"
                            #       f"\tAn Error occurred while waiting for sell order to be filled: {e}\n"
                            #       f"\tIGNORING ERROR...[{error_counter}]", end="")
                            # time.sleep(5)
                            continue
                    print(">>> sell order filled")
                else:
                    print(f"Order Error!")
                    print(sell_order)
                    input("press any key to continue...")
                    break


            # buy order logic
            quote_balance = get_balance(client, quote_currency)
            # print(f'NGN Balance: {ngn_balance}')

            if quote_balance < buy_Dollar_price:
                # i.e. balance is less than amount i want to buy 1  unit of USDT. then sell dolllar instead of buying dollar
                current_order = 'sell'

            if quote_balance > 0 and current_order == 'buy':
                buy_quantity = float(quote_balance) // float(buy_Dollar_price)
                # buy_order = place_buy_order(client, symbol, ngn_balance, buy_Dollar_price)
                buy_order = place_buy_order(client, symbol, buy_quantity, buy_Dollar_price)
                if buy_order is not None:
                    current_order = 'sell'
                    counter = 0
                    error_counter = 0
                    while True:
                        try:
                            counter += 1
                            ticker = client.get_ticker(symbol=symbol)
                            lp = Decimal(ticker['lastPrice'])
                            print(f"\r> Waiting for buy order to be filled...[{lp}]->[{buy_Dollar_price}] | [ {convert_seconds(counter)} ] | Error count = [{error_counter}]", end="")
                            time.sleep(1)
                            order_status = client.get_order(symbol=symbol, orderId=buy_order['orderId'])
                            if order_status['status'] == 'FILLED':
                                break
                        except Exception as e:
                            error_counter += 1
                            # print(f"\r> Waiting for buy order to be filled...[ {counter} ]\n"
                            #       f"\tAn Error occurred while waiting for by order to be filled: {e}\n"
                            #       f"\tIGNORING ERROR...[{error_counter}]", end="")
                            # time.sleep(5)
                            continue
                    print(">>> buy order filled")
                else:
                    print(f"Order Error!")
                    print(buy_order)
                    input("press any key to continue...")
                    break

            # wait for a minute before checking again
            print()
            print(f"An Order is successfully executed. cooling down to take the next order")
            print()
            total_completed_trade_cycle += 1
            time.sleep(30)

            if auto_mid_price is True:
                # recalculate the sell and buy dollar price
                mid_price = auto_calculate_mid_price()
                mid_price = float(mid_price)
                profit_margin = float(profit_margin)
                sell_Dollar_price = mid_price + profit_margin  # sell USDT at high price
                buy_Dollar_price = mid_price - profit_margin  # buy USDT at low price

                sell_Dollar_price = round(sell_Dollar_price, 1)
                buy_Dollar_price = round(buy_Dollar_price, 1)

            if auto_stake_amount is True:
                usd_bal = get_balance(client, base_currency)
                stake_dollar_amount = round((stake_dollar_percent / 100) * usd_bal)

        ans = input("press 't' to restart trading with current settings 'r' to restart trading with new settings Any other key to exit: ")
        if ans == 't':
            clear_screen()
            start_trading_loop(client)
        elif ans == 'r':
            clear_screen()
            change_settings()
            start_trading_loop(client)


    start_trading_loop(client)


except Exception as e:
    print(f"An Error Occurred: {e}")
    ans = input("Press any key to terminate: ")

