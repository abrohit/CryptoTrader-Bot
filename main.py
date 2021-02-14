import hmac, hashlib, base64, json, time, requests, math, dotenv, os

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

SELLVALUE = 63#Your upper RSI value.
BUYVALUE = 35#Your below RSI value.


dotenv_file = '.env'

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

key = os.environ['key']#Your CoinDcx key.

secret = os.environ['secret']#Your CoinDcx secret.
secret_bytes = bytes(secret, encoding='utf-8')

def GetRSI(ticker = 'BTCINR'):#Gets the RSI value of any ticker. BTCINR is default.

    url = 'https://in.tradingview.com/symbols/' + ticker + '/technicals/'

    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    driver = webdriver.Chrome('', options=option)#Selenium Path.
    driver.get(url)

    timeFrame = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[2]')
    timeFrame.click()

    time.sleep(0.5)
    
    soup=BeautifulSoup(driver.page_source,'lxml')
    
    driver.quit()
    
    RSI = float(soup.findAll("td", {"class": "cell-5XzWwbDG"})[1].get_text())
    return(RSI)
    

def GetQuantity(dp, currency = 'BTC'):#Gets the quantity of BTC owned. dp specifies the number of decimal places returned.
    
    timeStamp = int(round(time.time() * 1000))

    body = {
        "timestamp": timeStamp
        }

    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    
    url = 'https://api.coindcx.com/exchange/v1/users/balances'
    
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
        }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    for _ in data:
        if _['currency'] == currency:
            temp = _['balance'].split('.')
            return(float(temp[0] + '.' + temp[1][:dp]))

    return(None)

def Trade(action,quantity, type_ = 'market_order', currency = 'BTCINR', price = 0):#Trades based on the parameters provided.

    timeStamp = int(round(time.time() * 1000))

    body = {
        "side":"sell",
        "order_type": type_,
        "market": currency,
        "total_quantity": quantity,
        "price_per_unit": price,
        "timestamp": timeStamp
        }
    json_body = json.dumps(body, separators = (',', ':'))
    print(json_body)
    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
    
    url = 'https://api.coindcx.com/exchange/v1/orders/create'
    
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
        }
    
    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return(data)

above = False
below = False

run = False
while run:#The Main loop.
    
    RSI = GetRSI()

    if RSI > SELLVALUE:#Checks if the RSI value is greater than the sell value.
        above = True

    if RSI < BUYVALUE:#Checks if the RSI value is lesser than the buy value.
        below = True

    if RSI <= SELLVALUE and RSI >= BUYVALUE:#Checks if RSI is between the sell and buy values.
        if above:#Sells when RSI comesback down.
            BTCQuantity = GetQuantity(5)
            Trade('sell', BTCQuantity)
            above = False
        if below:#Buys when RSI increases again.
            INRQuantity = GetQuantity(1, 'INR')
            Trade('buy', INRQuantity)
            below = False
    
        
