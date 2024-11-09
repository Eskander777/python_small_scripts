import csv
import sys
from typing import Dict
import matplotlib.pyplot as plt
from datetime import date
from request_to_svdk import get_tarifs_from_svdk

months_dict = {
    "january": "Январь",
    "february": "Февраль",
    "march": "Март",
    "april": "Апрель",
    "may": "Май",
    "june": "Июнь",
    "july": "Июль",
    "august": "Август",
    "september": "Сентябрь",
    "october": "Октябрь",
    "november": "Ноябрь",
    "december": "Декабрь",
}


def gathering_info():
    """Gathering info about water spending"""
    month_names = months_dict.values()
    ru_month = ""
    while True:
        try:
            month = input('Введите месяц: ').title()
            if month == '':
                print('Выход из программы...')
                sys.exit()
            if month not in month_names:
                raise ValueError

            for eng_name, ru_name in months_dict.items():
                if ru_name == month:
                    month = eng_name
                    ru_month = ru_name

            month += ' ' + str(date.today().year)
            h_water_kitchen = int(input(
                'Введите данные по горячей воде на кухне: '))
            c_water_kitchen = int(input(
                'Введите данные по холодной воде на кухне: '))
            h_water_bathroom = int(input(
                'Введите данные по горяцей воде в ванной: '))
            c_water_bathroom = int(input(
                'Введите данные по холодной воде в ванной: '))
        except ValueError:
            print('Неправильно введены данные, попробуйте еще раз!')
        else:
            return month, h_water_kitchen, c_water_kitchen, h_water_bathroom, \
                c_water_bathroom, ru_month


def creating_csv_data_file(month, h_w_k, c_w_k, h_w_b, c_w_b):
    """First creation of CSV data file. Unused"""
    with open('water_data\water_data.csv', 'w') as file:
        writer = csv.DictWriter(
            file,
            fieldnames=['month',
                        'hot_water_kitchen',
                        'cold_water_kitchen',
                        'hot_water_bathroom',
                        'cold_water_bathroom',
                        'hot_water_used_in_month',
                        'cold_water_used_in_month'],
            quoting=csv.QUOTE_ALL
        )

        writer.writeheader()
        writer.writerow({
            'month': str(month),
            'hot_water_kitchen': str(h_w_k),
            'cold_water_kitchen': str(c_w_k),
            'hot_water_bathroom': str(h_w_b),
            'cold_water_bathroom': str(c_w_b),
            'hot_water_used_in_month': '0',
            'cold_water_used_in_month': '0'
        })


def read_csv_file():
    """Reading present CSV data file for calculations"""
    all_months = []
    with open('water_data\water_data.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_months.append(row)
    previous_month = all_months[-1]

    h_w_k_p = int(previous_month['hot_water_kitchen'])
    c_w_k_p = int(previous_month['cold_water_kitchen'])
    h_w_b_p = int(previous_month['hot_water_bathroom'])
    c_w_b_p = int(previous_month['cold_water_bathroom'])
    return h_w_k_p, c_w_k_p, h_w_b_p, c_w_b_p, all_months


def calculate_spending(month, h_w_k, c_w_k, h_w_b, c_w_b, h_w_k_p, c_w_k_p,
                       h_w_b_p, c_w_b_p):
    """Calculating water spending"""
    h_w_total = h_w_k + h_w_b
    c_w_total = c_w_k + c_w_b
    h_w_spent = h_w_total - (h_w_k_p + h_w_b_p)
    c_w_spent = c_w_total - (c_w_k_p + c_w_b_p)
    print('Всего горячей воды {}, холодной воды {}'.format(
        h_w_total, c_w_total))
    print('В {} было потрачено горячей воды - {} кубов, а холодной - {} кубов'
          .format(month, h_w_spent, c_w_spent))
    return h_w_spent, c_w_spent


def add_new_data_to_csv_file(month, h_w_k, c_w_k, h_w_b, c_w_b, h_w_spent,
                             c_w_spent):
    """Adding new data to present CSV data file"""
    with open('water_data\water_data.csv', 'a') as file:
        writer = csv.DictWriter(
            file,
            fieldnames=['month', 'hot_water_kitchen',
                        'cold_water_kitchen',
                        'hot_water_bathroom',
                        'cold_water_bathroom',
                        'hot_water_used_in_month',
                        'cold_water_used_in_month'],
            quoting=csv.QUOTE_ALL
        )
        writer.writerow({
            'month': str(month),
            'hot_water_kitchen': str(h_w_k),
            'cold_water_kitchen': str(c_w_k),
            'hot_water_bathroom': str(h_w_b),
            'cold_water_bathroom': str(c_w_b),
            'hot_water_used_in_month': str(h_w_spent),
            'cold_water_used_in_month': str(c_w_spent)
        })


def parse_water_values(water_dict: Dict) -> Dict:
    """Parse water data"""
    month_water_used = {}

    for key, value in water_dict.items():
        key_arr = key.split()
        month_name = months_dict[key_arr[0].strip()]
        new_key = month_name + " " + key_arr[-1]
        month_water_used[new_key] = value

    return month_water_used


def create_usage_graph(months_data):
    """Creates graphs of usage cold and hot water"""

    months_max = len(months_data)

    while True:
        try:
            print()
            months_entered = int(input(
                'Сколько месяцев вас интересует(Максимум {} месяцев): > '.format(months_max)))

            if months_entered == "":
                break

            months_num = int(months_entered)

            if months_num > months_max:
                raise

            hot_water_used_raw = {month['month']: int(month['hot_water_used_in_month'])
                                  for month in months_data[-months_num:]}
            cold_water_used_raw = {month['month']: int(month['cold_water_used_in_month'])
                                   for month in months_data[-months_num:]}

            hot_water_used = parse_water_values(hot_water_used_raw)
            cold_water_used = parse_water_values(cold_water_used_raw)

            fig = plt.figure()
            ax_hot_water = fig.add_subplot(211)
            ax_cold_water = fig.add_subplot(212)

            ax_hot_water.plot(hot_water_used.keys(),
                              hot_water_used.values(), c="red")
            ax_hot_water.margins(0)
            ax_hot_water.grid(axis='both')
            ax_hot_water.set_title('Горячая вода')

            ax_cold_water.plot(cold_water_used.keys(),
                               cold_water_used.values(), c="blue")
            ax_cold_water.margins(0)
            ax_cold_water.grid(axis='both')
            ax_cold_water.set_title('Холодная вода')

            fig.autofmt_xdate()
            fig.set_size_inches(15, 8)
            plt.show()

            break
        except:
            print()
            print('Ошибка, попробуйте еще раз')
            continue


def read_month(months):
    """Represented requested info from present CSV data file"""
    ru_months = [value for value in months_dict.values()]

    while True:
        print()
        picked_month = input(
            'Введите месяц и год, который вас интересует: ').title()
        if picked_month == '':
            print()
            print('Возврат в основное меню...')
            break

        enterd_arr = picked_month.split()
        ru_entered_name = enterd_arr[0]
        entered_year = enterd_arr[-1]

        if ru_entered_name not in ru_months:
            print()
            print(
                'Нет такого месяца! Попробуйте еще раз')
            continue

        for en_name, ru_name in months_dict.items():
            if ru_name == ru_entered_name:
                en_entered_name = en_name + " " + entered_year

                try:
                    month_data = next(
                        entity for entity in months if entity['month'] == en_entered_name)

                    hot_water_total = int(month_data['hot_water_kitchen']) \
                        + int(month_data['hot_water_bathroom'])
                    cold_water_total = int(month_data['cold_water_kitchen']) \
                        + int(month_data['cold_water_bathroom'])

                    print()
                    print('''В месяце {} года показатели такие: 
                    горячая вода на кухне - {} 
                    холодная вода на кухне - {}
                    горячая вода в ванной - {}
                    холодная вода в ванной - {}
                    всего горячая - {}
                    всего холодная - {}
                    израсходовано было холодной воды - {} кубов
                    израсходовано было горячей воды - {} кубов.'''
                          .format(picked_month,
                                  month_data['hot_water_kitchen'],
                                  month_data['cold_water_kitchen'],
                                  month_data['hot_water_bathroom'],
                                  month_data['cold_water_bathroom'],
                                  hot_water_total,
                                  cold_water_total,
                                  month_data['cold_water_used_in_month'],
                                  month_data['hot_water_used_in_month'])
                          )

                    try:
                        print("Получение тарифов с сайта...")
                        print()
                        dates, drink_water, canalization = get_tarifs_from_svdk()
                        print(
                            '''Актуальные тарифы на даты {}: 
                                питьевая вода(холодная) - {} руб/куб, 
                                канализация - {} руб/куб.'''.format(dates, drink_water, canalization)
                        )
                    except TypeError:
                        print('Что-то пошло не так! Невозможно загрузить тарифы.')

                    break
                except StopIteration:
                    print('Таких данных нет! Попробуйте еще раз')
                    continue


def main():
    h_w_k_p, c_w_k_p, h_w_b_p, c_w_b_p, all_months = read_csv_file()
    while True:
        choice = input('''
Чтобы вы хотели сделать:  1. Прочитать ранее внесенные данные
                          2. Показать график расхода воды
                          3. Внести новые данные
                          4. Выход
                          > ''')

        if choice == '1':
            read_month(all_months)
        elif choice == '2':
            create_usage_graph(all_months)
        elif choice == '3':
            try:
                month, h_w_k, c_w_k, h_w_b, c_w_b, ru_month = gathering_info()
            except UnboundLocalError:
                pass
            else:
                h_w_spent, c_w_spent = calculate_spending(ru_month,
                                                          h_w_k,
                                                          c_w_k,
                                                          h_w_b,
                                                          c_w_b,
                                                          h_w_k_p,
                                                          c_w_k_p,
                                                          h_w_b_p,
                                                          c_w_b_p)
                add_new_data_to_csv_file(month, h_w_k, c_w_k, h_w_b, c_w_b,
                                         h_w_spent, c_w_spent)
        else:
            print('Выход из программы...')
            break


if __name__ == '__main__':
    main()
