import json
import requests
import random
from getuseragent import UserAgent
from colorama import Fore, init

init(autoreset=True)
ua = UserAgent("android")
useragent = random.choice(ua.list)


def get_token(query, tg_user_id, proxy=None):
    headers = {
        "telegram-user-id": tg_user_id,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": "ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    url = 'https://wuffitap-05-api.wuffi.io/v1/public-api/login-telegram'
    data_json = json.dumps(
        {
            "initData": query
        }
    )
    try:
        if proxy is None:
            response = requests.post(url, headers=headers, data=data_json)
        else:
            response = requests.post(url, headers=headers, data=data_json, proxies=proxy)
        return response.json()
    except json.JSONDecodeError as j:
        print(f"{Fore.RED}Ошибка при декодировании JSON ответа: {j}")
        return None
    except requests.HTTPError as http_err:
        print(f"{Fore.RED}HTTP ошибка: {http_err}")
        return None
    except requests.RequestException as req_err:
        print(f"{Fore.RED}Ошибка запроса: {req_err}")
        return None
    except Exception as ex:
        print(f"{Fore.RED}Неизвестная ошибка: {ex}")
        return None


def farm_tap(access_token, tg_user_id, taps, start_time, end_time, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": access_token,
        "telegram-user-id": tg_user_id,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": "ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    url = 'https://wuffitap-05-api.wuffi.io/v1/protected-api/tap'
    data_json = json.dumps(
        {
            "taps": taps,
            "startTime": start_time,
            "endTime": end_time
        }
    )
    try:
        if proxy is None:
            response = requests.post(url, headers=headers, data=data_json)
        else:
            response = requests.post(url, headers=headers, data=data_json, proxies=proxy)
        return response.json()
    except json.JSONDecodeError as j:
        print(f"{Fore.RED}Ошибка при декодировании JSON ответа: {j}")
        return None
    except requests.HTTPError as http_err:
        print(f"{Fore.RED}HTTP ошибка: {http_err}")
        return None
    except requests.RequestException as req_err:
        print(f"{Fore.RED}Ошибка запроса: {req_err}")
        return None
    except Exception as ex:
        print(f"{Fore.RED}Неизвестная ошибка: {ex}")
        return None


def user_login(query, tg_user_id, proxy=None, access_token=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "telegram-user-id": tg_user_id,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": "ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    if access_token is not None:
        headers['authorization'] = access_token
    url = 'https://wuffitap-05-api.wuffi.io/v1/public-api/login-telegram'
    data_json = json.dumps(
        {
            "initData": query
        }
    )
    try:
        if proxy is None:
            response = requests.post(url, headers=headers, data=data_json)
        else:
            response = requests.post(url, headers=headers, data=data_json, proxies=proxy)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError as j:
        print(f"{Fore.RED}Ошибка при декодировании JSON ответа: {j}")
        return None
    except requests.HTTPError as http_err:
        print(f"{Fore.RED}HTTP ошибка: {http_err}")
        return None
    except requests.RequestException as req_err:
        print(f"{Fore.RED}Ошибка запроса: {req_err}")
        return None
    except Exception as ex:
        print(f"{Fore.RED}Неизвестная ошибка: {ex}")
        return None

