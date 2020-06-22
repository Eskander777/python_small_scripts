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
    months_total_sums = []
    months_total_names = []
    with open(file) as f:
        data = f.readlines()
    months_data = list(filter(lambda line: '#' in line, data))
    for month in months_data:
        month_split_data = month.split()
        month_total_name = month_split_data[3]
        month_total_rubs = month_split_data[4]
        month_total_kops = month_split_data[6]
        month_total_sum = f'{month_total_rubs}.{month_total_kops}'
        months_total_names.append(month_total_name)
        months_total_sums.append(float(month_total_sum))
    months_names_sums = dict(zip(months_total_names, months_total_sums))
    return months_names_sums


def creates_graph(data_dict):
    """Creates graph according to data_dict"""
    months = list(data_dict.keys())
    summs = list(data_dict.values())
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Сумма руб')
    ax.axhspan(11000, 16000, facecolor='#b9ed9f')
    ax.axhspan(16001, 20000, facecolor='#f6f78d')
    ax.axhspan(20001, max(summs) + 500, facecolor='#ff776b')
    ax.margins(0)

    plt.title('Общие траты в:')
    plt.grid()
    ax.plot(months, summs, color='black', linewidth=2)
    fig.autofmt_xdate()
    plt.show()


def write_data_to_file(sums, name):
    """Shows results and writes it to file"""
    months = ['Январе', 'Феврале', 'Марте', 'Апреле', 'Мае', 'Июне', 'Июле',
              'Августе', 'Сентябре', 'Октябре', 'Ноябре', 'Декабре']
    total = round(sum(sums), 2)
    total_rub = int(total // 1)
    total_kop = int(round((total % 1) * 100))
    rubs = get_rubles(total_rub)
    kops = get_kops(total_kop)
    stat_month = datetime.datetime.now().month - 2
    month_to_write = months[stat_month]
    data = f'# Всего в {month_to_write}: {total_rub} {rubs}, {total_kop} {kops}\n'
    print()
    print(data)
    with open(name, 'a') as f:
        f.write(data)


def main():
    while True:
        choice = input('''Что бы вы хотели посчитать: 1. общая сумма за месяц
                            2. общая сумма за месяц переведенная
                           > ''')

        if choice == '1':
            name = FILES[0]
        elif choice == '2':
            name = FILES[1]
        else:
            break
        try:
            data = count_money_month_data(name)
            # write_data_to_file(data, name)
            data_in_dict = get_complete_statistics(name)
            creates_graph(data_in_dict)
        except UnboundLocalError:
            print('Неправильный ввод!')


if __name__ == '__main__':
    main()
