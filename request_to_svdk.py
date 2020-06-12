from requests import get
from html2text import html2text


def get_tarifs_from_svdk():
    """Get tariffs form svdk.ru"""
    try:
      response = get(
          'https://www.mup-vodokanal-sochi.ru/abonent/tariffs').text
      data_str = html2text(response)
      list_data = data_str.strip().split(', ')
      for line in list_data:
          if 'с 01.01.2020 по 30.06.2020' in line:
              line_list = line.splitlines()
              for nums in line_list:
                  if 'с 01.01.2020 по 30.06.2020' in nums and '24,06' not in nums:
                      nums_list = nums.split(' | ')
                      active_dates = nums_list[1]
                      price_water = float(nums_list[3].replace(',', '.'))
                      price_canalization = float(nums_list[-2].replace(',', '.'))
                      return active_dates, price_water, price_canalization
    except TypeError:
      print('Что-то пошло не так!')

# Dummy approach
# data_part = list_data[1].splitlines()
# data_part_numbers_list = data_part[-5].split(' | ')
# # print(data_part_numbers_list)

# price_water = float(data_part_numbers_list[3].replace(',', '.'))
# price_canalization = float(data_part_numbers_list[-2].replace(',', '.'))

# print(price_water)
# print(price_canalization)
