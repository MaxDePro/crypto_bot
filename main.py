from tokens import cmc_token
import json
import requests


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


def main():
    get_cmc_data('BTC')


if __name__ == '__main__':
    main()
