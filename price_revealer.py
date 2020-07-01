from decimal import Decimal, DecimalException, DivisionByZero
import sys


class TruePrice:
    def __init__(self, shop_price, shop_amount):
        self.shop_price = shop_price
        self.shop_amount = shop_amount

    def reveal_true_price(self):
        self.one_gramm_cost = self.shop_price / self.shop_amount
        ten_gramm_cost = round((self.one_gramm_cost * 10), 2)
        fifty_gramm_cost = round((self.one_gramm_cost * 50), 2)
        hundred_gramm_cost = round((self.one_gramm_cost * 100), 2)

        print(
            f'\nВ магазине за {self.shop_price} грамм просят {self.shop_amount} руб.')
        print(f'\t100 грамм стоит {hundred_gramm_cost} руб')
        print(f'\t50 грамм стоит {fifty_gramm_cost} руб')
        print(f'\t10 грамм стоит {ten_gramm_cost} руб')

    def calculate_gramms(self):
        """Выводит сумму указанного количества грамм"""
        gramms_interested_str = input(
            'Цена какого количества грамм вас интересует: '
        )
        try:
            result = round((Decimal(gramms_interested_str)
                            * self.one_gramm_cost), 2)
            print(f'За {gramms_interested_str} грамм будет {result} руб.')
        except:
            print('Неправильно введены данные!')


def main():
    """Основная операция"""
    while True:
        try:
            shop_price_str = input(
                '\nВведите цену в магазине в рублях(нажмите "ENTER" чтобы выйти): > ').replace(',', '.')
            if shop_price_str != '':
                shop_price = Decimal(shop_price_str)
            elif shop_price_str == '':
                break
            shop_amount_str = input(
                'Введите количество грамм(нажмите "ENTER" чтобы выйти): > ').replace(',', '.')
            if shop_amount_str != '':
                shop_amount = Decimal(shop_amount_str)
            elif shop_amount_str == '':
                break
            true_price = TruePrice(shop_price, shop_amount)
            true_price.reveal_true_price()
        except (DecimalException, DivisionByZero):
            print('\nНеправильно внесены данные. Попробуйте еще раз.')
        else:
            choice = input(
                '\nХотели бы вы узнать цену определенного количества грамм? "y"- да, "n"-нет: >  '
            )
            if choice == 'y':
                true_price.calculate_gramms()
                choice_continue = input(
                    'Хотели бы продолжить? ("y"- да, "n"-нет): > ')
                if choice_continue == 'y':
                    continue
                else:
                    break
            else:
                break


if __name__ == '__main__':
    main()
