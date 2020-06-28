import os
import math
from decimal import Decimal, DecimalException
from datetime import datetime
from rubs_kops_functions import get_rubles, get_kops
import csv


class Money():
    checks = []
    goods_l = []
    fieldnames = [
        'date',
        'road_money',
        'work_money',
        'food_work_money',
        'total']

    def __init__(self):
        while True:
            amount = input("\nСумма чека: > ").replace(',', '.')
            if amount == '':
                break
            try:
                self.checks.append(Decimal(amount))
                while True:
                    amount_l = input(
                        "Стоимость товаров, которые исчисляются из чека: > ").replace(',', '.')
                    if amount_l == '':
                        break
                    self.goods_l.append(Decimal(amount_l))
            except DecimalException:
                print('Неправильный ввод, попробуйте еще раз.\n')
                self.checks.clear()
        self.summ = sum(self.checks)
        self.summ_removed = sum(self.goods_l)
        self.fixed_summ = self.summ - self.summ_removed

        self.fixed_summ_rub = self.fixed_summ // 1
        self.fixed_summ_kop = int((self.fixed_summ % 1) * 100)

        self.fixed_summ_part = self.fixed_summ / 2
        self.part_rub = self.fixed_summ_part // 1
        self.part_kop = math.ceil((self.fixed_summ_part % 1) * 100)

        rubles = get_rubles(self.fixed_summ_rub)
        rubles_p = get_rubles(self.part_rub)
        kops = get_kops(self.fixed_summ_kop)
        kops_p = get_kops(self.part_kop)

        print(
            f"\nОбщая сумма: {self.fixed_summ_rub} {rubles}, {self.fixed_summ_kop} {kops}.")
        print(
            f"Перевести нужно: {self.part_rub} {rubles_p}, {self.part_kop} {kops_p}.")

        self.writedown()
        if self.summ_removed != 0:
            self.writedown_removed()

    def writedown_removed(self):
        with open(os.path.join('money_data_for_oop', 'outcome_removed.csv'), 'a') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=self.fieldnames,
                quoting=csv.QUOTE_ALL
            )
            writer.writerow({'date': str(datetime.now().date()),
                             'road_money': '0',
                             'work_money': '0',
                             'food_work_money': str(self.summ_removed),
                             'total': str(self.summ_removed)
                             })

    def writedown(self):
        write_part = str(Decimal(self.part_kop) / 100 + self.part_rub)
        date_time = str(datetime.now().strftime('%A, %d.%m.%Y %H:%M'))

        instance_t = date_time + ' - ' + str(self.fixed_summ)
        instance_r = date_time + ' - ' + write_part

        with open(os.path.join('money_data_for_oop', 'outcome_total.txt'), 'a') as o_t:
            o_t.write(instance_t + '\n')
        with open(os.path.join('money_data_for_oop', 'outcome_half.txt'), 'a') \
                as outcome:
            outcome.write(instance_r + '\n')


def main():
    money = Money()


if __name__ == '__main__':
    main()
