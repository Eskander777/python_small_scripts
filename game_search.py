import requests
from argparse import ArgumentParser


def search_and_find_game():
    """Takes game and searches it"""
    parser = ArgumentParser()
    parser.add_argument(
        '--game', help='Type the game price you want to find')
    args = parser.parse_args()
    if not args.game:
        game_asked = input('Какая игра интересует? ').lower()
    elif args.game:
        game = args.game.lower().join('_')
        game_asked = game
    url = 'http://www.plati.io/api/search.ashx?query=' + game_asked \
          + '&pagesize=100&response=json'
    r = requests.get(url)
    print("Status code:", r.status_code)
    return r


def take_and_show(r):
    """Showing results of searching"""
    dict_r = r.json()
    games = dict_r['items']
    prices = []
    print('Response Headers')
    for name, info in r.headers.items():
        print(name, '-', info)
    print('-' * 45)
    for item in games:
        try:
            print('Name:', item['name'])
            print('Price in rub', item['price_rur'])
            print('Price in usd', item['price_usd'])
            prices.append(item['price_rur'])
            print('URL:', item['url'])
        except UnicodeEncodeError:
            print('В названии использованы нечитаемые символы!')
            continue
        print()
    try:
        print('Максимальная цена:', max(prices))
        print('Минимальная цена:', min(prices))
        print('Всего игр:', len(games))
    except ValueError:
        print('Такой игры нет!')


def main():
    r = search_and_find_game()
    take_and_show(r)


if __name__ == '__main__':
    main()
