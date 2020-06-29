import requests
import xmltodict
from decimal import *


class Cbr_Calculator():

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
                    f"{val['Nominal']} {val['Name']} стоит в рублях {val['Value']}" for val in self.currencies_list]
                print(
                    f"Список доступных валют по курсу ЦБР к рублю на {xml_data['ValCurs']['@Date']}:\n")
                for cur in self.cur_nominals_names:
                    print(f"{(self.cur_nominals_names.index(cur) + 1)}. {cur}")


calc = Cbr_Calculator()
