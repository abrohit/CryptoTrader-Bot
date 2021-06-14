<h1 align="center">Crypto Trader Bot</h1>
<p align="center">
  Trades Cryptocurrency automatically!
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents
* [About the Project](#about-the-project)
* [Setting up the Project](#setting-up-the-project)
* [Tech Stack](#tech-stack)
* [Contact](#contact)

## About the Project

A very simple bot that only trades based on the RSI value. It's simple strategy is to buy when RSI value comes back up(you can choose the buy back RSI value) and sell when the RSI goes back down(you can choose the RSI sell value). With basic testing I have seen anywhere between 3% to 7% returns daily. This would be different for different cryptocurrencies. Use this bot at your OWN RISK. 

## Setting up the Project

After downloading the script, replace the [key](https://github.com/abrohit/CryptoTrader-Bot/blob/main/main.py#L18) and [secret](https://github.com/abrohit/CryptoTrader-Bot/blob/main/main.py#L20) on line 18 and 20 respectively with your key and secret from Coindcx.

Make sure to change [run = False](https://github.com/abrohit/CryptoTrader-Bot/blob/main/main.py#L106) on line 106 to `run = True` to make sure the main loop runs.

## Tech Stack
- Python
- Selenium
- BeautifulSoup
- CoinDCX API

## Contact

Twitter : [abrohit05](https://twitter.com/abrohit05)

LinkedIn : [Rohit Manjunath](https://www.linkedin.com/in/rohitmanjunath/)

Website : [abrohit](https://abrohit.pythonanywhere.com/)

