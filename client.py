import socket
from config import SERVER, PORT, DEBUG

# Function to display the UI
def show_menu():
    print("\n--- Stock Trading Game ---")
    print("0. Menu")
    print("1. Buy Stock")
    print("2. Sell Stock")
    print("3. View Portfolio")
    print("4. View Stock Price")
    print("5. View Market Overview")
    print("6. Exit")
    print("---------------------------\n")

# Function to send orders to the server and wait for responses
def game_loop(client_socket):
    show_menu()

    while True:
        action = input("Enter your choice (press \"0\" to see menu): ").strip()

        if action == "0":
            show_menu()
            continue

        elif action == "1":
            # Request available stock symbols from the server
            client_socket.send("STOCKS".encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Available stocks: {response}")
            stock_symbol = input("Enter stock symbol to buy: ").upper()
            quantity = int(input(f"Enter the quantity of {stock_symbol} to buy: "))
            order = f"BUY {stock_symbol} {quantity}"
            client_socket.send(order.encode('utf-8'))
        
        elif action == "2":
            # Request available stock symbols from the server
            client_socket.send("STOCKS".encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Available stocks: {response}")
            stock_symbol = input("Enter stock symbol to sell: ").upper()
            quantity = int(input(f"Enter the quantity of {stock_symbol} to sell: "))
            order = f"SELL {stock_symbol} {quantity}"
            client_socket.send(order.encode('utf-8'))

        elif action == "3":
            # View portfolio
            client_socket.send("PORTFOLIO".encode('utf-8'))

        elif action == "4":
            stock_symbol = input("Enter stock symbol to get the price: ").upper()
            order = f"PRICE {stock_symbol}"
            client_socket.send(order.encode('utf-8'))

        elif action == "5":
            # View market overview
            client_socket.send("MARKET".encode('utf-8'))

        elif action == "6":
            print("Exiting the game...")
            client_socket.send("EXIT".encode('utf-8'))
            break

        else:
            print("Invalid action, try again.")
            continue

        # Block until we receive a response from the server
        response = client_socket.recv(1024).decode('utf-8')
        if response:
            print(f"\n{response}")

# Main function to connect to the server and start the client
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        client_socket.connect((SERVER, PORT))
        print(f"Connected to the server at {SERVER}:{PORT}")
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        return

    try:
        # Handle user input for buying/selling stocks
        game_loop(client_socket)
    except KeyboardInterrupt:
        pass # Gracefully exit

if __name__ == "__main__":
    start_client()
