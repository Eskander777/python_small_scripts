import requests
from html2text import html2text

name = input('Введите название игры для поиска в Steam: ')
name_list = name.split()
name_list_len = len(name_list)
symbols_to_remove = [':']
name_to_search = name.lower()
first_word_of_name = name_list[0]

for symbol in symbols_to_remove:
    name_to_search = name_to_search.replace(symbol, "")
    name_to_search = name_to_search.replace("-", " ")

name_to_search_list = name_to_search.split()
search_name = "+".join(name_to_search_list)

query_params = '/search/?term={}'.format(search_name)

response = requests.get(
    'https://store.steampowered.com/{}'.format(query_params)
).text

data = html2text(response)
data_list = data.split()

first_word_index = data_list.index(first_word_of_name)
name_form_steam = data_list[first_word_index: first_word_index + name_list_len]
print(name_form_steam)
rub_word_index = data_list.index('pуб.')

rub_indeсes_list = [i for i, val in enumerate(data_list) if val == '1']
list_iterator = iter(rub_indeсes_list)

if first_word_index > rub_word_index:
    second_rub_word_index = next(list_iterator)
    print(second_rub_word_index)
    game_elements_array = data_list[first_word_index:second_rub_word_index + 1]
else:
    game_elements_array = data_list[first_word_index:rub_word_index + 1]


print(game_elements_array)
