from rubs_kops_functions import get_rubles


def count_free_money(income, other, savings):
    income = int(income)
    left_money = income - other
    free_money_d = int(left_money / 30)
    savings_d = int(savings / 30)
    free_money = int(free_money_d - savings_d)
    return free_money
    

def count_savings(income, other):
    income = int(income)
    left_money = income - other
    savings = int((left_money * 8) / 100)
    return savings


def main():
    number_1 = "\nУкажите ежемесячный доход"
    number_1 += "\n(нажмите 'enter', чтобы закрыть программу): "
    number_2 = "Укажите обязательные расходы за месяц: "

    while True:
        try:
            income = input(number_1)
            
            if income == '':
                break
            
            other = int(input(number_2))
        except ValueError:
            print('Неправильный ввод, попробуйте еще раз.')
            continue
        else:
            savings = count_savings(income, other)
            free_money = count_free_money(income, other, savings)
                
            rubles = get_rubles(free_money)
            rubles_s = get_rubles(savings)
            
            if free_money <= 300:
                print("\nВам нужно уменьшить свои расходы или увеличить "
                      "доходы:)")
            
            else:
                print("\nВ день вы можете тратить до", free_money, rubles,
                      "и не занимать денег!")
                print("\nОткладывать вы можете по", savings, rubles_s,
                      "в месяц.")
                break


if __name__ == '__main__':
    main()
