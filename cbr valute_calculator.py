import requests
import xmltodict
from decimal import *


def get_cbr_info():
    """Get CBR info from XML data"""
    response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
    xml_data = xmltodict.parse(response.text)
    currencies_list = xml_data['ValCurs']['Valute']
    cur_names = [cur['Nominal'] + ' ' + cur['Name'] for cur in currencies_list]
    print('Список доступных валют по курсу ЦБР к рублю на',
          xml_data['ValCurs']['@Date'] + ':')
    print('-' * 45)
    for currency in cur_names:
        print(str(cur_names.index(currency) + 1) + '.', currency)
    return cur_names, currencies_list


def user_interface_data(cur_names, currencies_list):
    """Takes information from user and prepares everything"""
    print('-' * 45)
    cur_to_pick = input('Выберите валюту по номеру в таблице: > ')
    if cur_to_pick == '':
        return cur_to_pick, 0, 0, 0, 0
    else:
        cur_to_pick = int(cur_to_pick)
        cur_picked = cur_names[cur_to_pick - 1]
        cur_picked_list = cur_picked.split()
        num_cur_picked_from_list = Decimal(cur_picked_list.pop(0))
        name_cur_picked = ' '.join(cur_picked_list)
        print()
        cur_picked_value = 0
        for val in currencies_list:
            if val['Nominal'] + ' ' + val['Name'] == cur_picked:
                cur_picked_value = Decimal(val['Value'].replace(',', '.'))

        cur_operation = input(f"""Вы хотели бы узнать отношение: 
        1.Валюта {name_cur_picked} к рублю
        2 Рубля к валюте {name_cur_picked}
        >  """)
        if cur_operation == '1' or cur_operation == '2':
            cur_amount = Decimal(
                input(f'Введите количество единиц выбранной валюты: ').replace(',', '.'))
            return name_cur_picked, cur_operation, cur_amount, cur_picked_value, num_cur_picked_from_list
        else:
            raise ValueError


def represents_results(name_cur_picked, cur_operation,
                       cur_amount, cur_picked_value, num_cur_picked_from_list):
    """Represents results"""
    if cur_operation == '1':
        if num_cur_picked_from_list != 1:
            cur_amount /= num_cur_picked_from_list
        count_result = round(cur_amount * cur_picked_value, 2)
        num_cur_picked = round(num_cur_picked_from_list * cur_amount, 2)
        print(num_cur_picked, name_cur_picked, '=', count_result, 'руб')
    elif cur_operation == '2':
        count_result = cur_amount / cur_picked_value
        num_cur_picked = round(num_cur_picked_from_list * count_result, 2)
        print(round(cur_amount, 2), 'руб', '=', num_cur_picked,
              name_cur_picked)


def main():
    cur_names, currencies_list = get_cbr_info()
    while True:
        try:
            name_cur_picked, cur_operation, cur_amount, cur_picked_value, num_cur_picked_from_list  \
                = user_interface_data(cur_names, currencies_list)
            if name_cur_picked == '':
                print('Выход из приложения...')
                break
        except (ValueError, IndexError):
            print('Ошибка, поробуйте еще раз!')
            continue
        else:
            represents_results(name_cur_picked, cur_operation,
                               cur_amount, cur_picked_value, num_cur_picked_from_list)


if __name__ == '__main__':
    main()
