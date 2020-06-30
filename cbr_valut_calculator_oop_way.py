import requests
import xmltodict
from decimal import *


class Cbr_Calculator:

    def __init__(self):
        try:
            response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
        except:
            print('Connection Error. Check your internet connection or try again later.')
        else:
            try:
                xml_data = xmltodict.parse(response.content)
            except:
                print('Parsing data error.')
            else:
                self.currencies_list = xml_data['ValCurs']['Valute']
                self.cur_nominals_names = [
                    f"{val['Nominal']} {val['Name']}" for val in self.currencies_list]
                print(
                    f"Список доступных валют по курсу ЦБР к рублю на {xml_data['ValCurs']['@Date']}:\n")
                for cur in self.cur_nominals_names:
                    print(f"{(self.cur_nominals_names.index(cur) + 1)}. {cur}")

    def user_interface_data(self):
        """Takes information from user and prepares everything"""
        print('-' * 45)
        cur_to_pick = input('Выберите валюту по номеру в таблице: > ')
        if cur_to_pick == '':
            return cur_to_pick
        else:
            cur_to_pick = int(cur_to_pick)
            cur_picked = self.cur_nominals_names[cur_to_pick - 1]
            cur_picked_list = cur_picked.split()
            num_cur_picked_from_list = Decimal(cur_picked_list.pop(0))
            name_cur_picked = ' '.join(cur_picked_list)
            print()
            cur_picked_value = 0
            for val in self.currencies_list:
                if val['Nominal'] + ' ' + val['Name'] == cur_picked:
                    cur_picked_value = Decimal(val['Value'].replace(',', '.'))

            cur_operation = input(f"""Вы хотели бы узнать отношение: 
            1.Валюта {name_cur_picked} к рублю
            2 Рубля к валюте {name_cur_picked}
            >  """)
            if cur_operation == '1' or cur_operation == '2':
                cur_amount = Decimal(
                    input(f'Введите количество единиц выбранной валюты: ').replace(',', '.'))
                data_dict = {
                    'name_cur_picked': name_cur_picked,
                    'cur_operation': cur_operation,
                    'cur_amount': cur_amount,
                    'cur_picked_value': cur_picked_value,
                    'num_cur_picked_from_list': num_cur_picked_from_list
                }
                return data_dict
            else:
                raise ValueError


def represents_results(info: tuple):
    """Represents results"""
    if info['cur_operation'] == '1':
        if info['num_cur_picked_from_list'] != 1:
            info['cur_amount'] /= info['num_cur_picked_from_list']
        count_result = round(info['cur_amount'] * info['cur_picked_value'], 2)
        num_cur_picked = round(
            info['num_cur_picked_from_list'] * info['cur_amount'], 2)
        print(
            f"{num_cur_picked} {info['name_cur_picked']} = {count_result} руб")
    elif info['cur_operation'] == '2':
        count_result = info['cur_amount'] / info['cur_picked_value']
        num_cur_picked = round(
            info['num_cur_picked_from_list'] * count_result, 2)
        print(round(info['cur_amount'], 2), 'руб', '=', num_cur_picked,
              info['name_cur_picked'])


def main():
    calc = Cbr_Calculator()
    while True:
        try:
            data = calc.user_interface_data()
            if data == '':
                print('Выход из приложения...')
                break
        except (ValueError, IndexError):
            print('Ошибка, поробуйте еще раз!')
            continue
        else:
            represents_results(data)


if __name__ == '__main__':
    main()
