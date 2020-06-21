import requests
import html2text


def get_data():
    '''Get all neccesary information from web. And puts it in an list'''
    response = requests.get(
        'http://autodr.ru/autospravka/559-avtomobilnye-kody-regionov-rossii.html')
    response_content = response.content.decode(response.apparent_encoding)
    response_array = html2text.html2text(response_content).splitlines()
    shortened_array = response_array[response_array.index(
        'Республика Адыгея | **01**  '):response_array.index('Выше приведен список кодов регионов, из которого можно узнать: - автокоды') - 1]
    codes_and_regions = []
    for line in shortened_array:
        try:
            region = line[:line.index('|')]
            code = line[line.index('|') + 1:].replace('**',
                                                      '').replace(',', '').split()
            region_and_code = {'region': region,
                               'code': code}
            codes_and_regions.append(region_and_code)
        except ValueError:
            pass

    return codes_and_regions


def search_for_region_by_code(data):
    '''Searches region by entered code'''
    right_region = False
    while True:
        right_region = False
        code_to_search = input(
            '\nВедите код, у которого вы бы хотели узнать регион: ')
        if code_to_search == '':
            break
        else:
            for region in data:
                if code_to_search in region['code']:
                    right_region = region['region']
                    print(
                        f'Машинный номер {code_to_search} у региона {right_region}')

            if not right_region:
                print(f'Нет такого кода: {code_to_search}')

            answer = input('\nХотите попробовать снова? (y/n): ')
            if answer == 'y':
                continue
            else:
                break


def main():
    data = get_data()
    search_for_region_by_code(data)


if __name__ == '__main__':
    main()
