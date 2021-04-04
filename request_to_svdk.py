from requests import get
from bs4 import BeautifulSoup
from datetime import datetime


def get_data_from_line(line):
    tags = line.find_all('p')
    data = [p.text for p in tags if p != None]
    return data


def get_tarifs_from_svdk():
    """Get tariffs form svdk.ru"""
    try:
        response = get(
            'https://www.mup-vodokanal-sochi.ru/abonent/tariffs').text

        soup = BeautifulSoup(response, "html.parser")
        table = soup.find('table')
        table_data = table.tbody.find_all('tr')

        today = datetime.today()
        data = get_data_from_line(table_data[-2])

        if today > datetime(2021, 6, 30):
            data = get_data_from_line(table_data[-1])

        return data[1], data[3], data[-2]

        # for line in list_data:
        #     if 'с 01.01.2020 по 30.06.2020' in line:
        #         line_list = line.splitlines()
        #         for nums in line_list:
        #             if 'с 01.01.2020 по 30.06.2020' in nums and '24,06' not in nums:
        #                 nums_list = nums.split(' | ')
        #                 active_dates = nums_list[1]
        #                 price_water = float(nums_list[3].replace(',', '.'))
        #                 price_canalization = float(
        #                     nums_list[-2].replace(',', '.'))
        # return active_dates, price_water, price_canalization
    except TypeError:
        print('Что-то пошло не так!')
