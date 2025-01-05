import socket
import threading
import random
import time
import configparser

# Read server configuration from the config file
config = configparser.ConfigParser()
config.read("config.ini")

# Server settings from the config file
SERVER = config["server"]["host"]
PORT = int(config["server"]["port"])

# Dictionary to hold stock prices
stock_prices = {
    "AAPL": 150,
    "GOOG": 2800,
    "TSLA": 700,
    "AMZN": 3300
}

# Dictionary to hold client portfolios
client_portfolios = {}

# Function to update stock prices periodically
def update_stock_prices():
    while True:
        for stock in stock_prices:
            # Simulate stock price changes
            stock_prices[stock] += random.randint(-5, 5)
        time.sleep(3)

# Function to handle client requests
def handle_client(client_socket, client_address):
    print(f"Client {client_address} connected.")
    
    # Initialize client portfolio
    client_portfolios[client_address] = {}

    while True:
        try:
            # Receive client message
            message = client_socket.recv(1024).decode('utf-8')

            if message == "STOCKS":
                # Send available stock symbols to the client
                available_stocks = ", ".join(stock_prices.keys())
                client_socket.send(f"{available_stocks}\n".encode('utf-8'))

            elif message.startswith("BUY"):
                # Example: BUY AAPL 10
                parts = message.split()
                stock_symbol = parts[1]
                quantity = int(parts[2])

                if stock_symbol not in stock_prices:
                    client_socket.send(f"Invalid stock symbol: {stock_symbol}\n".encode('utf-8'))
                elif quantity <= 0:
                    client_socket.send(f"Invalid quantity: {quantity}\n".encode('utf-8'))
                else:
                    # Add stock to portfolio
                    if stock_symbol in client_portfolios[client_address]:
                        client_portfolios[client_address][stock_symbol] += quantity
                    else:
                        client_portfolios[client_address][stock_symbol] = quantity
                    client_socket.send(f"Successfully bought {quantity} of {stock_symbol}.\n".encode('utf-8'))

            elif message.startswith("SELL"):
                # Example: SELL AAPL 5
                parts = message.split()
                stock_symbol = parts[1]
                quantity = int(parts[2])

                if stock_symbol not in client_portfolios[client_address] or client_portfolios[client_address][stock_symbol] < quantity:
                    client_socket.send(f"Not enough {stock_symbol} in your portfolio to sell.\n".encode('utf-8'))
                elif quantity <= 0:
                    client_socket.send(f"Invalid quantity: {quantity}\n".encode('utf-8'))
                else:
                    # Remove stock from portfolio
                    client_portfolios[client_address][stock_symbol] -= quantity
                    client_socket.send(f"Successfully sold {quantity} of {stock_symbol}.\n".encode('utf-8'))

            elif message.startswith("PORTFOLIO"):
                # Show portfolio
                portfolio = client_portfolios[client_address]
                response = "Your portfolio:\n"
                for stock, quantity in portfolio.items():
                    price = stock_prices.get(stock, "Unknown")
                    response += f"{stock}: {quantity} shares, current price: {price}\n"
                client_socket.send(response.encode('utf-8'))

            elif message.startswith("PRICE"):
                # Example: PRICE AAPL
                parts = message.split()
                stock_symbol = parts[1]

                if stock_symbol in stock_prices:
                    price = stock_prices[stock_symbol]
                    client_socket.send(f"The price of {stock_symbol} is {price}.\n".encode('utf-8'))
                else:
                    client_socket.send(f"Stock {stock_symbol} not found.\n".encode('utf-8'))

            elif message.startswith("MARKET"):
                # Show entire market
                response = "Market Overview:\n"
                for stock, price in stock_prices.items():
                    response += f"{stock}: {price}\n"
                client_socket.send(response.encode('utf-8'))

            elif message.startswith("EXIT"):
                # Exit
                print(f"Client {client_address} disconnected.")
                client_socket.close()
                break

            else:
                client_socket.send("Invalid command.\n".encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            break

# Function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER, PORT))
    server_socket.listen(5)
    print(f"Stock trading server listening on port {PORT}...")

    # Start stock price update thread
    threading.Thread(target=update_stock_prices, daemon=True).start()

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    start_server()
