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
    while True:
        cur_to_pick = int(input('Выберите валюту по номеру в таблице: > '))
        try:
            cur_picked = cur_names[cur_to_pick - 1]
        except Exception:
            print('Такой валюты в списке нет! Попробуйте еще раз.')
            print()
            continue
        else:
            print()
            cur_picked_value = 0
            for val in currencies_list:
                if val['Nominal'] + ' ' + val['Name'] == cur_picked:
                    cur_picked_value = Decimal(val['Value'].replace(',', '.'))

            cur_operation = input("""Вы хотели бы узнать отношение: 
            1.Выбранной валюты к рублу
            2 Рубля к выбранной валюте
            >  """)
            cur_amount = Decimal(input('Введите количество единиц валюты: ').replace(',', '.'))
            return cur_picked, cur_operation, cur_amount, cur_picked_value


def represents_results(cur_picked, cur_operation,
                       cur_amount, cur_picked_value):
    """Represents results"""
    cur_picked_list = cur_picked.split()
    num_cur_picked_from_list = Decimal(cur_picked_list.pop(0))
    name_cur_picked = ' '.join(cur_picked_list)

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
    try:
        cur_picked, cur_operation, cur_amount, cur_picked_value \
            = user_interface_data(cur_names, currencies_list)
    except Exception:
        pass
    else:
        represents_results(cur_picked, cur_operation, cur_amount, cur_picked_value)


if __name__ == '__main__':
    main()
