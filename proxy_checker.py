import requests
from colorama import Fore, init

init(autoreset=True)


def proxy_checker(proxy):
    url = 'http://httpbin.org/ip'
    proxies = {
        'http': proxy,
        'https': proxy
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Прокси - {proxy} валид")
            return True
        return False
    except Exception as ex:
        print(f"Прокси вернуло ошибку: {ex}")
        return False


def checkout_list_proxy(data):
    for acc in data:
        proxy_data = acc['proxy']
        if proxy_data == '':
            r = input(
                Fore.RED + f"Аккаунт: {acc['number']}. Отсутствует прокси. Вы хотите продолжить? (y/n):\n").strip().lower()
            if r == 'n':
                exit()
        elif proxy_checker(acc['proxy']):
            print(Fore.CYAN + f"Аккаунт: {acc['number']}. Прокси валид")
        else:
            print(Fore.RED + f"Аккаунт: {acc['number']}. Прокси не валид")
            exit()
