# Stocket 📈🔌

A socket-based terminal (for now) stock market simulator. The higher-order vision is to have a web-based UI with graphs (who doesn't love graphs).

To get started make sure you have installed Python package dependencies (will get a requirements.txt or something up at some point).

.env.MY_APP_ENV defines the server URL and port configuration into `SERVER`, `PORT`.

`python ./server.py [optional APP_ENV={PROD|DEV}]` will open a socket at `SERVER:PORT` and listen for incoming connection requests. The server script is non-interactable.

It serves data from a `stock_prices` dictionary that updates the stock prices (values) at its symbols (keys) randomly in an `update_stock_prices` thread.

`python ./client.py [optional APP_ENV={PROD|DEV}]` connects to the server sockets and--once connected--initiates a command line input session with the user.

From the client, the user can select one of the following actions by typing the action index (i.e. "0" will display the menu).

0. **Menu**                      --  _Displays the action options._
1. **Buy Stock**                --  _Tries to buy X units of a stock symbol S into the user portfolio. Only succeeds if the symbol is found and the user has sufficient capital._
2. **Sell Stock**                --  _Tries to sell X units of a stock symbol S from the user portfolio. Only success if the symbol is found and the user has sufficient stock._
3. **View Portfolio**            --  _Displays the user portfolio._
4. **View Stock Price**          --  _Displays the current price of a stock S._
5. **View Market Overview**      --  _Displays all of the stock symbols on the server and their prices._
