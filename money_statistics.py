from rubs_kops_functions import *
import matplotlib.pyplot as plt
import datetime

FILES = ['money_data\outcome_total.txt', 'money_data\outcome_sashka.txt']


def count_money_month_data(name):
    """Counts and sums up money data"""
    sums = []
    with open(name) as f:
        data = f.readlines()
    restart = True
    while restart:
        restart = False
        for line_raw in data:
            if line_raw.startswith('#'):
                del data[:data.index(line_raw) + 1]
                restart = True
                break
    for line in data:
        line_l = line.split()
        if line_l != []:
            sum_l = float(line_l[-1])
            sums.append(sum_l)
    return sums


def get_complete_statistics(file):
    """Gets and parses statistics of all months"""
    if file == FILES[1]:
        with open(file, encoding='utf-8') as f:
            data = f.readlines()
    elif file == FILES[0]:
        with open(file) as f:
            data = f.readlines()

    months_data = list(filter(lambda line: '#' in line, data))
    months_split_data = list(map(lambda m: m.split(), months_data))

    months_total_names = [month[3] for month in months_split_data]
    months_total_sums = [
        float(f'{month[4]}.{month[6]}') for month in months_split_data]
    months_names_sums = dict(zip(months_total_names, months_total_sums))
    return months_names_sums


def creates_graph(data_dict, file):
    """Creates graph according to data_dict"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    months = list(data_dict.keys())
    summs = list(data_dict.values())
    if file == FILES[1]:
        ax.axhspan(5000, 9000, facecolor='#b9ed9f')
        ax.axhspan(9001, 11000, facecolor='#f6f78d')
        ax.axhspan(11001, 15000, facecolor='#ff776b')
    elif file == FILES[0]:
        ax.axhspan(11000, 16000, facecolor='#b9ed9f')
        ax.axhspan(16001, 20000, facecolor='#f6f78d')
        ax.axhspan(20001, max(summs) + 500, facecolor='#ff776b')
    year = datetime.datetime.now().year
    ax.set_ylabel('Сумма руб')
    ax.margins(0)

    plt.title(f'Общие траты в {year} в:')
    plt.grid()
    ax.plot(months, summs, color='black', linewidth=2)
    fig.autofmt_xdate()
    plt.show()


def write_data_to_file(sums, name):
    """Shows results and writes it to file"""
    months = ['Январе', 'Феврале', 'Марте', 'Апреле', 'Мае', 'Июне', 'Июле',
              'Августе', 'Сентябре', 'Октябре', 'Ноябре', 'Декабре']
    total = round(sum(sums), 2)
    total_rub, total_kop = int(total // 1), int(round((total % 1) * 100))
    rubs, kops = get_rubles(total_rub), get_kops(total_kop)
    stat_month = datetime.datetime.now().month - 2
    month_to_write = months[stat_month]
    data = f'# Всего в {month_to_write}: {total_rub} {rubs}, {total_kop} {kops}\n'
    print()
    print(data)
    with open(name, 'a') as f:
        f.write(data)


def main():
    while True:
        print()
        choice = input('''Что бы вы хотели посчитать: 1. общая сумма за месяц
                            2. общая сумма за месяц переведенная
                           > ''')

        if choice == '1':
            name = FILES[0]
        elif choice == '2':
            name = FILES[1]
        elif choice == '':
            print('Выход из программы...')
            break
        else:
            print('Неправильный ввод, попробуйте еще раз! Нажмите "ENTER" для выхода')
            continue
        try:
            data = count_money_month_data(name)
            write_data_to_file(data, name)
            data_in_dict = get_complete_statistics(name)
            creates_graph(data_in_dict, name)
        except UnboundLocalError:
            print('Неправильный ввод!')


if __name__ == '__main__':
    main()
