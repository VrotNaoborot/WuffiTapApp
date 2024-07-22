import random
import threading
import time
from math import ceil
from requests_data import *
import csv
from colorama import Fore, init
from proxy_checker import *
import urllib

init(autoreset=True)

DATA_FILE = "data.csv"


def reader_data():
    with open(DATA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        rows = list(reader)
        return rows


def generate_times(previous_end_time=None):
    # Если предыдущего endTime нет, устанавливаем startTime на текущее время
    if previous_end_time is None:
        start_time = int(time.time() * 1000)
    else:
        # Устанавливаем startTime чуть позже, чем предыдущий endTime
        start_time = previous_end_time + random.randint(100, 500)  # Разница в пределах 100 миллисекунд

    # Определяем разницу для endTime от 1.5 до 4 секунд
    delta = random.uniform(1.2, 3.0)  # Разница в секундах
    end_time = start_time + int(delta * 1000)  # Преобразуем в миллисекунды
    return start_time, end_time


def farming(dns, color, name, curr_energy_balance, access_token, tg_user_id, proxy):
    current_energy = curr_energy_balance
    prev_time = None
    if current_energy > 300:
        print(f"{color}[{name}] Фарминг начался...")
        while current_energy > 300:
            start_time, end_time = generate_times(prev_time)
            prev_time = end_time
            time.sleep(3)
            taps = random.randint(1, 50)
            farm_resp = farm_tap(dns=dns, access_token=access_token, tg_user_id=tg_user_id, taps=taps,
                                 start_time=start_time,
                                 end_time=end_time, proxy=proxy)
            if farm_resp is not None and 'currentEnergy' in farm_resp:
                # print(f"Отправлено {taps}")
                current_energy = farm_resp['currentEnergy']
                # print(f"Баланс: {current_energy}")
            else:
                # print("Ошибка")
                continue
        else:
            print(f"{color}[{name}] Фарминг закончился...")


def account_farming(dns, name, access_token, tg_user_id, proxy):
    color_account = random.choice(
        [Fore.CYAN, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.BLACK, Fore.MAGENTA, Fore.RESET, Fore.WHITE,
         Fore.LIGHTMAGENTA_EX])

    tap_config_response = tap_config(dns=dns, tg_user_id=tg_user_id, access_token=access_token, proxy=proxy)
    user_tap_count_tokens = 1
    energy_limit = 3000
    potion = 1
    if tap_config_response is not None and 'userPointIncreasePerTapConfig' in tap_config_response:
        user_tap_count_tokens = tap_config_response['userPointIncreasePerTapConfig']['basedValue']
        energy_limit = tap_config_response['energyLimit']['basedValue']
        potion = tap_config_response["energyIncreasePerSecConfig"]['basedValue']
        print(f"{color_account}[{name}] Получена информация о конфиге")
    elif tap_config_response is not None and 'error' in tap_config_response:
        print(f"{Fore.RED}[{name}] {tap_config_response}")
        exit()
    else:
        print(f"{color_account}[{name}] Не удалось получить информацю о конфиге. {tap_config_response}")
    current_energy = 0

    while True:
        daily_checkin_resp, daily_code = daily_checkin(dns, tg_user_id=tg_user_id, access_token=access_token,
                                                       proxy=proxy)
        if daily_checkin_resp is not None and daily_code == 200:
            for day in daily_checkin_resp:
                if day.get("status", 0) == 1:
                    id = day["id"]
                    name = day["name"]
                    count = day['description']
                    claim_resp, claim_code = daily_claim(dns, tg_user_id=tg_user_id, task_id=id,
                                                         access_token=access_token, proxy=proxy)
                    if claim_resp is not None and "id" in claim_resp and claim_code == 200:
                        print(f"{color_account}[{name}] {name}: Получено: {count}")

        tap_response = tap_status(dns=dns, tg_user_id=tg_user_id, access_token=access_token, proxy=proxy)
        if tap_response is not None and 'currentEnergy' in tap_response:
            current_energy = tap_response['currentEnergy']
            print(f"{color_account}[{name}] Баланс: {tap_response['totalPawsEarned']}")
            print(f"{color_account}[{name}] Текущая энергия: {tap_response['currentEnergy']}")
        else:
            print(f"{color_account}[{name}] Не удалось получить tap_response. {tap_response}")
        # делаем клик для обновления энергии
        start_time, end_time = generate_times()
        print(f"{color_account}[{name}] Обновляем информацию об энергии")
        time.sleep(3)
        farm_resp = farm_tap(dns=dns, access_token=access_token, tg_user_id=tg_user_id, taps=random.randint(1, 4),
                             start_time=start_time,
                             end_time=end_time, proxy=proxy)
        if farm_resp is not None and 'currentEnergy' in farm_resp:
            current_energy = farm_resp['currentEnergy']
            print(f"{color_account}[{name}] Энергия: {current_energy}")
        else:
            print(f"{color_account}[{name}] Не удалось обновить информацию об энергии. {farm_resp}")
        # bot farming
        estimate_response = estimate_earned(dns=dns, tg_user_id=tg_user_id, access_token=access_token, proxy=proxy)
        if estimate_response is not None:
            if 'code' in estimate_response and estimate_response['code'] == 200 and estimate_response[
                'message'] == "Success":
                print(
                    f"{color_account}[{name}] TapBot добыл {estimate_response['data']['estimated_earned']} токенов.")
                claim_response = claim_bot(dns=dns, tg_user_id=tg_user_id, access_token=access_token, proxy=proxy)
                if claim_response is not None and claim_response['code'] == 200 and claim_response[
                    'message'] == "Success":
                    print(f"{color_account}[{name}] Токены получены.")
                else:
                    print(f"{color_account}[{name}] Не удалось получить токены")
            elif 'message' in estimate_response and estimate_response['message'] == "User has no activated TapBot!":
                print(f"{color_account}[{name}] TapBot не активирован")
            else:
                print(f"{color_account}[{name}] Estimate_response вернуло: {estimate_response}")
        else:
            print(f"{color_account}[{name}] estimate_earned вернуло None")

        farming(dns=dns, color=color_account, name=name, curr_energy_balance=current_energy, access_token=access_token,
                tg_user_id=tg_user_id, proxy=proxy)
        buff_resp = buff(dns=dns, tg_user_id=tg_user_id, access_token=access_token, proxy=proxy)

        if buff_resp is not None and 'instant_fill' in buff_resp:
            count_instant_fill = buff_resp['instant_fill']['total_usage_left']
            count_nitro_taps = buff_resp['nitro_taps']['total_usage_left']
            print(f"{color_account}[{name}] Буст энергии: {count_instant_fill}")
            print(f"{color_account}[{name}] Буст нитро: {count_nitro_taps}")
            if count_instant_fill > 0:
                using_fill_resp = using_buff(dns=dns, tg_user_id=tg_user_id, access_token=access_token, proxy=proxy,
                                             number_buff=2)
                if using_fill_resp is not None and 'instant_fill' in using_fill_resp:
                    print(f"{color_account}[{name}] Восстановление энергии использовано.")
                    farming(dns=dns, color=color_account, name=name, curr_energy_balance=current_energy,
                            access_token=access_token, tg_user_id=tg_user_id, proxy=proxy)
            if count_nitro_taps > 0:
                while count_nitro_taps > 0:
                    using_nitro_resp = using_buff(dns=dns, tg_user_id=tg_user_id, access_token=access_token,
                                                  proxy=proxy, number_buff=1)
                    if using_nitro_resp is not None and 'nitro_taps' in using_nitro_resp:
                        print(f"{color_account}[{name}] Nitro использован")
                        count_nitro_taps -= 1
                        prev_time = None
                        for i in range(7):
                            start_time, end_time = generate_times(prev_time)
                            time.sleep(3)
                            taps = random.randint(5, 50)
                            farm_resp = farm_tap(dns=dns, access_token=access_token, tg_user_id=tg_user_id, taps=taps,
                                                 start_time=start_time,
                                                 end_time=end_time, proxy=proxy)

                            prev_time = end_time
                    else:
                        print(f"{color_account}[{name}] Не удалось использовать бафф")
        else:
            print(buff_resp)
        time_sleep = ceil(energy_limit / potion)
        print(f"{color_account}[{name}] Спим {time_sleep} секунд...")
        time.sleep(time_sleep)


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
    print(f"{Fore.CYAN}Проверка данных...")
    for acc in data:
        query = None if acc['query'] == "" else acc["query"]
        access_token = None if acc['access_token'] == "" else acc['access_token']
        proxy = None if acc['proxy'] == "" else {'http': acc['proxy'], 'https': acc['proxy']}
        telegram_user_id = acc['tg_user_id']
        if telegram_user_id == '':
            print(f"{Fore.RED}Аккаунт {acc['number']} не указан tg_user_id")
            exit()
        if query is None:
            print(f"{Fore.RED}Аккаунт {acc['number']} не указан query")
            exit()
        if access_token is None:
            print(f"{Fore.CYAN}Аккаунт: {acc['number']} получаем access_token...")
            dns_response = dns_resolver(tg_user_id=telegram_user_id, proxy=proxy)
            if dns_response is not None and 'dns' in dns_response:
                login_resp = user_login(dns=dns_response['dns'], query=query, tg_user_id=telegram_user_id, proxy=proxy,
                                        access_token=access_token)
                if login_resp is not None and 'token' in login_resp:
                    acc['access_token'] = login_resp['token']
                    data_changed = True
                elif "error" in login_resp and login_resp['error'] == "Unauthorized app URL":
                    print(f"{Fore.RED}Аккаунт: {acc['number']} Cf bypass")
                    exit()
                else:
                    print(f"{Fore.RED}Не удалось получить access_token. {login_resp}")
                    exit()
            else:
                print(f"{Fore.RED}Аккаунт: {acc['number']} не удалось получить dns от сервера.")
                exit()

        # if (access_token is None and query is not None) or (access_token is not None and query is not None):
        #     print(f"{Fore.CYAN}Аккаунт: {acc['number']} получаем access_token...")
        #     login_resp = user_login(query, tg_user_id=telegram_user_id, proxy=proxy, access_token=access_token)
        #     if login_resp is not None and 'token' in login_resp:
        #         acc['access_token'] = login_resp['token']
        #         data_changed = True
        #     elif "error" in login_resp and login_resp['error'] == "Unauthorized app URL":
        #         print(f"{Fore.RED} Аккаунт: {acc['number']} Cf bypass")
        #         exit()
        #     elif login_resp is None or ('message' in login_resp and login_resp['401: Unauthorized']): # если не правильный access_token, пытаемся без него
        #         second_log_resp = user_login(query=query, tg_user_id=telegram_user_id, proxy=proxy)
        #         if second_log_resp is not None and 'token' in second_log_resp:
        #             acc['access_token'] = login_resp['token']
        #             data_changed = True
        #         else:
        #             print(f"{Fore.RED}Аккаунт: {acc['number']} не удалось получить access_token. Обновите query")
        #             exit()
        #     else:
        #         print(f"{Fore.RED}Не удалось получить токен. {login_resp}")
        #         exit()
        # elif query is None and access_token is None:
        #     print(f"{Fore.RED}На аккаунте {acc['number']} отсутствует query и access_token")
        #     exit()

    if data_changed:
        with open(DATA_FILE, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)
            print(f"{Fore.CYAN}Токены записаны")

    data = reader_data()
    threads = []
    for acc_user in data:
        if acc_user['query'].startswith("user"):
            user_data = acc_user['query'].split('&')[0].split('=')[1]
        else:
            user_data = acc_user['query'].split('&')[1].split('=')[1]
        user_info = urllib.parse.unquote(user_data)
        user_info = json.loads(user_info)

        username = user_info.get('username', 'Unknown')
        access_token = acc_user['access_token']
        tg_user_id = acc_user['tg_user_id']
        proxy = None if acc_user['proxy'] == '' else {'http': acc_user['proxy'], 'https': acc_user['proxy']}
        dns_response = dns_resolver(tg_user_id=tg_user_id, proxy=proxy)
        if dns_response is not None and 'dns' in dns_response:
            thread = threading.Thread(target=account_farming,
                                      args=(dns_response['dns'], username, access_token, tg_user_id, proxy))
            threads.append(thread)
            thread.start()
        else:
            print(f"{Fore.RED}[{username}] Не удалось получить dns")
            print(dns_response)
            exit()

    for thread in threads:
        thread.join()


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
