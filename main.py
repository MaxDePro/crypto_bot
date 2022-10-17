from tokens import cmc_token
import json
import requests
import re

from flask import Flask
from flask import request
from flask import Response

from flask_sslify import SSLify

tg_token = '5683031385:AAE6DMBta9hWgo_WpmTVNXQXqe9xafEKjpI'

app = Flask(__name__)
sslify = SSLify(app)


def write_json(data, filename='response.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_cmc_data(crypto):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
        'symbol': crypto,
        'convert': 'USD'
    }
    headers = {'X-CMC_PRO_API_KEY': cmc_token}

    r = requests.get(url, headers=headers, params=params).json()

    price = r['data'][crypto]['quote']['USD']['price']
    print(price)


def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']

    pattern = r"/[a-zA-Z]{2,4}"

    ticker = re.findall(pattern, txt)

    if ticker:
        symbol = ticker[0][1:].upper()
    else:
        symbol = ''

    return chat_id, symbol


def send_message(chat_id, text='bla-bla'):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    r = requests.post(url, json=payload)
    return r


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, symbol = parse_message(msg)

        if not symbol:
            send_message(chat_id, text='Wrong data')
            return Response('Ok', status=200)

        price = get_cmc_data(symbol)
        send_message(chat_id, price)
        write_json(msg, 'telegram_request.json')
        return Response('Ok', status=200)
    else:
        return '<h1>Coinmarketup Bot</h1>'


def main():
    # TODO BOT

    # 1. Locally create a basic Flask application
    # 2. Send up a tunnel
    # 3. Set a webhook
    # 4. Receive and parse a user's  message
    # 5. Send message to a user

    get_cmc_data('BTC')

    # https://api.telegram.org/bot5683031385:AAE6DMBta9hWgo_WpmTVNXQXqe9xafEKjpI/getMe
    # https://api.telegram.org/bot5683031385:AAE6DMBta9hWgo_WpmTVNXQXqe9xafEKjpI/sendMessage?chat_id=392888619&text=Hello human



if __name__ == '__main__':
    # main()
    app.run(debug=True, port=5005)
