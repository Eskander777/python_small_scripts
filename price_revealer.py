from decimal import Decimal, DecimalException
import sys


def reveal_true_price():
    """Высчитывает настоящую цену продуктов"""
    shop_price_str = input('Введите цену в магазине: ')
    shop_amount_str = input('Введите количество грамм: ')
    try:
        one_gramm_cost = Decimal(shop_price_str) / Decimal(shop_amount_str)
        ten_gramm_cost = round((one_gramm_cost * 10), 2)
        fifty_gramm_cost = round((one_gramm_cost * 50), 2)
        hundred_gramm_cost = round((one_gramm_cost * 100), 2)
        return shop_price_str, shop_amount_str, one_gramm_cost, \
            ten_gramm_cost, fifty_gramm_cost, hundred_gramm_cost
    except (DecimalException, TypeError):
        print('Неправильные данные!')


def show_results(price, amount, one, ten, fifty, hundred):
    """Выводит информацию о результатах"""
    print('''В магазане за {} грамм просят {} руб. 
    100 грамм стоит {} руб
    50 грамм стоит {} руб
    10 грамм стоит {} руб
    1 грамм стоит {} руб'''.format(price, amount, hundred, fifty, ten,
                                   round(one, 2)))


def calculate_gramms(one):
    """Выводит сумму указанного количества грамм"""
    gramms_interested_str = input(
        'Цена какого количества грамм вас интересует: '
    )
    try:
        result = Decimal(gramms_interested_str) * one
        print('За {} грамм будет {} руб'.format(gramms_interested_str,
                                                round(result, 2)))
    except Exception:
        print('Неправильно введены данные!')


def main():
    """Основная операция"""
    try:
        price, amount, one, ten, fifty, hundred = reveal_true_price()
    except Exception:
        sys.exit()
    else:
        show_results(price, amount, one, ten, fifty, hundred)
        print()
        choice = input(
            "Хотели бы вы узнать цену определенного количества грамм? "
            "1 - да; 2 - нет: "
        )
        if choice == '1':
            calculate_gramms(one)


if __name__ == '__main__':
    main()
