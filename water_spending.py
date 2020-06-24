import csv
import sys
import matplotlib.pyplot as plt
from datetime import date
from request_to_svdk import get_tarifs_from_svdk


def gathering_info():
    """Gathering info about water spending"""
    month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май',
                   'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                   'Ноябрь', 'Декабрь']
    while True:
        try:
            month = input('Введите месяц: ').title()
            if month == '':
                print('Выход из программы...')
                sys.exit()
            if month not in month_names:
                raise ValueError
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
                c_water_bathroom


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
    months = []
    with open('water_data\water_data.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            months.append(row)
    previous_month = months[-1]
    h_w_k_p = int(previous_month['hot_water_kitchen'])
    c_w_k_p = int(previous_month['cold_water_kitchen'])
    h_w_b_p = int(previous_month['hot_water_bathroom'])
    c_w_b_p = int(previous_month['cold_water_bathroom'])
    return h_w_k_p, c_w_k_p, h_w_b_p, c_w_b_p, months


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


def create_usage_graph(months_data):
    """Creates graphs of usage cold and hot water"""
    hot_water_used = {month['month']: int(month['hot_water_used_in_month'])
                      for month in months_data}
    cold_water_used = {month['month']: int(month['cold_water_used_in_month'])
                       for month in months_data}

    fig = plt.figure()
    ax_hot_water = fig.add_subplot(211)
    ax_cold_water = fig.add_subplot(212)
    ax_hot_water.plot(hot_water_used.keys(), hot_water_used.values(), c="red")
    ax_hot_water.margins(0)
    ax_cold_water.plot(cold_water_used.keys(),
                       cold_water_used.values(), c="blue")
    ax_cold_water.margins(0)
    fig.autofmt_xdate()
    plt.show()


def read_month(months):
    """Represented requested info from present CSV data file"""
    entered_months = [month['month'] for month in months]
    tariffs = None
    try:
        dates, drink_water, canalization = get_tarifs_from_svdk()
        tariffs = '''Актуальные тарифы на даты {}: 
                    питьевая вода(холодная) - {} руб/куб, 
                    канализация - {} руб/куб.'''.format(dates, drink_water, canalization)
    except TypeError:
        print('Что-то пошло не так! Невозможно загрузить тарифы.')
    while True:
        picked_month = input(
            'Введите месяц и год, который вас интересует: ').title()
        print()
        if picked_month == '':
            print('Возврат в основное меню...')
            print()
            break
        elif picked_month not in entered_months:
            print('Такой месяц еще не внесен! Попробуйте еще раз!')
            print()
            continue
        else:
            for month in months:
                if picked_month in month.values():
                    hot_water_total = int(month['hot_water_kitchen']) \
                        + int(month['hot_water_bathroom'])
                    cold_water_total = int(month['cold_water_kitchen']) \
                        + int(month['cold_water_bathroom'])
                    if tariffs is not None:
                        print(tariffs)
                    print('''В месяце {} года показатели такие: 
                    горячая вода на кухне - {} 
                    холодная вода на кухне - {}
                    горячая вода в ванной - {}
                    холодная вода в ванной - {}
                    всего горячая - {}
                    всего холодная - {}
                    израсходовано было холодной воды - {} кубов
                    израсходовано было горячей воды - {} кубов.'''
                          .format(month['month'],
                                  month['hot_water_kitchen'],
                                  month['cold_water_kitchen'],
                                  month['hot_water_bathroom'],
                                  month['cold_water_bathroom'],
                                  hot_water_total,
                                  cold_water_total,
                                  month['cold_water_used_in_month'],
                                  month['hot_water_used_in_month'])
                          )
        break


def main():
    while True:
        choice = input('''
Чтобы вы хотели сделать:  1. Прочитать ранее внесенные данные
                          2. Добавить новые данные
                          3. Выход
                          > ''')

        h_w_k_p, c_w_k_p, h_w_b_p, c_w_b_p, months = read_csv_file()

        if choice == '1':
            create_usage_graph(months)
            read_month(months)
        elif choice == '2':
            try:
                month, h_w_k, c_w_k, h_w_b, c_w_b = gathering_info()
            except UnboundLocalError:
                pass
            else:
                h_w_spent, c_w_spent = calculate_spending(month,
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
