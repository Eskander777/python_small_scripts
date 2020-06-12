def get_rubles(summ):
    """Gives right words for rubles"""
    summ_str = str(summ)
    if summ_str.endswith(('0', '5', '6', '7', '8', '9', '10', '11', '12',
                          '13', '14', '15', '16', '17', '18', '19')):
        return 'рублей'
    elif summ_str.endswith('1'):
        return 'рубль'
    elif summ_str.endswith(('2', '3', '4')):
        return 'рубля'


def get_kops(summ):
    """Gives right word for kopeks"""
    summ_str = str(summ)
    if summ_str.endswith(('0', '5', '6', '7', '8', '9', '10', '11', '12',
                          '13', '14', '15', '16', '17', '18', '19')):
        return 'копеек'
    elif summ_str.endswith('1'):
        return 'копейка'
    elif summ_str.endswith(('2', '3', '4')):
        return 'копейки'
