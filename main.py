import telegram
import pandas as pd
import ta.momentum
import time
import os
import requests

TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
bot = telegram.Bot(token=TOKEN)
alerted = False

while True:
    try:
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=50"
        data = requests.get(url).json()
        df = pd.DataFrame(data, columns=['time','open','high','low','close','volume','close_time','quote_vol','trades','taker_buy_base','taker_buy_quote','ignore'])
        df['close'] = pd.to_numeric(df['close'])
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        rsi = df['rsi'].iloc[-2]   # 마감된 직전 캔들
        price = df['close'].iloc[-2]

        if rsi <= 20 and not alerted:
            bot.send_message(chat_id=CHAT_ID,
                text=f"비트코인 5분봉 RSI {rsi:.1f} 터치!!\n가격 ≈ ${price:,.0f} USD")
            alerted = True
        if rsi > 25:
            alerted = False

        time.sleep(60)
    except:
        time.sleep(60)
