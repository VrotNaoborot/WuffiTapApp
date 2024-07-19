from requests_data import *
import csv
from colorama import Fore, init
from proxy_checker import *

init(autoreset=True)

DATA_FILE = "data.csv"


def reader_data():
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        rows = list(reader)
        return rows


def main():
    say_hello()
    data = reader_data()
    if len(data) == 0:
        print(f"{Fore.RED}Отсутствуют данные для аккаунтов")
        exit()

    print("Проверка прокси")
    checkout_list_proxy(data)

    data_changed = False
    # Проверка всех аккаунтов
    for acc in data:
        query = None if acc['query'] == "" else acc["query"]
        access_token = None if acc['access_token'] == "" else acc['access_token']
        proxy = None if acc['proxy'] == "" else acc['proxy']
        telegram_user_id = acc['tg_user_id']
        if telegram_user_id == '':
            print(f"{Fore.RED}Аккаунт {acc['number']} не указан tg_user_id")
            exit()
        if query is None and access_token is None:
            print(f"{Fore.RED}На аккаунте {acc['number']} отсутствует query и access_token")
            exit()
        elif access_token is None and query is not None:
            print(f"{Fore.CYAN}Аккаунт: {acc['number']} получаем access_token...")
            login_resp = user_login(query, tg_user_id=telegram_user_id, proxy=proxy, access_token=access_token)
            if login_resp is not None and 'token' in login_resp:
                acc['access_token'] = login_resp['token']
                data_changed = True
            else:
                print(f"{Fore.RED}Не удалось получить токен.")
                exit()

    if data_changed:
        with open(DATA_FILE, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)
            print(f"{Fore.CYAN}Токены записаны")


def say_hello():
    print(Fore.BLUE + r"""  _____                  
 |  __ \                 
 | |__) |_ _ _ __  _   _ 
 |  ___/ _` | '_ \| | | |
 | |  | (_| | | | | |_| |
 |_|   \__,_|_| |_|\__,_|                             
""")
    print(Fore.CYAN + "Questions - https://t.me/Panunchik")
    print(Fore.CYAN + "GitHub - https://github.com/VrotNaoborot")


if __name__ == '__main__':
    main()
