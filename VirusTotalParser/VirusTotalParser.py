import requests
import time
import os
import sys


def scan_a_file_by_virustotal(apikey):
    path = os.path.join(os.path.dirname(__file__), 'VirusTotal_data')
    try:
        filenames = os.listdir(path)
    except FileNotFoundError:
        print('There is no such file or directory!')
    else:
        file_to_scan = os.path.join(path, filenames[0])
        url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        params = {'apikey': apikey}
        files = {'file': ('myfile', open(file_to_scan, 'rb'))}
        started = time.time()
        response = (requests.post(url, files=files, params=params))
        response_json = response.json()
        print('Time spent {:.2f} sec'.format(time.time() - started))
        print('Response status code is {}'.format(response.status_code))
        print('MD5 = {}'.format(response_json['md5']))
        print('SHA-1 = {}'.format(response_json['sha1']))
        print('SHA-256 = {}'.format(response_json['sha256']))
        print('Message from VirusTotal: {}'.format(
            response_json['verbose_msg']))
        return response_json


def check_for_scanreport(apikey, file_scan=None):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    if file_scan is None:
        resource = input('Enter a meaning you want to analyse >:  ')
    else:
        resource = file_scan['md5']
    try:
        params = {'apikey': apikey, 'resource': resource}
    except UnboundLocalError as e:
        print(e)
    else:
        started = time.time()
        response = requests.get(url, params=params)
        try:
            response_json = response.json()
            total_scans = response_json['total']
        except KeyError:
            print(response.content.decode())
        except TypeError as e:
            print(e)
        else:
            print('Time spent {:.2f} sec'.format(time.time()-started))
            print('Response status code is {}'.format(response.status_code))
            print('Total scans: {}'.format(total_scans))
            print('Positive threats: {}'.format(response_json['positives']))
            scan_results = response_json['scans'].items()
            if response_json['positives'] > 0:
                for antivir, result in scan_results:
                    print('\t', antivir, 'Result:', result['result'])
            else:
                print('Anti-viruses used:')
                for antivirus, _ in scan_results:
                    print('\t', antivirus)


def check_list_meanings_in_virustotal(apikey):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    path = os.path.join(os.path.dirname(__file__), 'VirusTotal_data_list')
    try:
        filenames = os.listdir(path)
        list_to_scan = os.path.join(path, filenames[0])
    except (FileNotFoundError, UnboundLocalError):
        print('There is no such file or directory!')
    else:
        with open(list_to_scan, 'r') as file:
            lines_to_scan = file.readlines()
        if len(list_to_scan) == 0:
            print('There is no text in the file')
        else:
            started = time.time()
            for line in lines_to_scan:
                line = line.rstrip('\n')
                params = {'apikey': apikey, 'resource': line}
                response = requests.get(url, params=params)
                try:
                    response_json = response.json()
                    total_scans = response_json['total']
                except KeyError:
                    print('Meaning:', line)
                    print(response.content.decode())
                    print()
                else:
                    print('Meaning:', line)
                    print('Total scans: {}'.format(total_scans))
                    print('Positive threats: {}'.format(
                        response_json['positives']))
                    print()
            print('Total time spent {:.2f} sec'.format(time.time() - started))


def main():
    apikey = '9d7778a02ab45579253769d72b0d74bf071f7efea5f8ac365c0e7738f55ce137'
    while True:
        choice = input('''
        What would you like to do: 
        1. Check using MD5 or SHA-1 or SHA-256 meanings
        2. Check file in 'VirusTotal_data' folder
        3. Check meanings list using .txt file in folder "VirusTotal_data_list" 
        4. Exit
        > ''')
        if choice == '1':
            check_for_scanreport(apikey)
        elif choice == '2':
            file_scan = scan_a_file_by_virustotal(apikey)
            print()
            check_for_scanreport(apikey, file_scan)
        elif choice == '3':
            check_list_meanings_in_virustotal(apikey)
        else:
            sys.exit()


if __name__ == '__main__':
    main()
