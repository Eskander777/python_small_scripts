import csv
import os


csv_file = os.path.join('E:\Desktop\ines.csv')
file_to_write = os.path.join('E:\Desktop\ile_1.txt')

with open(csv_file) as file_csv:
    parsed_file = csv.DictReader(file_csv, fieldnames=['name',
                                                       'description',
                                                       'condition',
                                                       'launch_type',
                                                       'enter_by_name'])

    for service in parsed_file:
        if service['description'] == '':
            service['description'] = 'No description'
        if service['launch_type'] == 'Вручную' or \
                service['enter_by_name'] == 'Вручную':
            pass
        else:
            info_to_write = str(service['name']) + ' - ' \
                            + str(service['description'])
            with open(file_to_write, 'a') as f_w:
                f_w.write(info_to_write + '\n')
