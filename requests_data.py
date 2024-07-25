import json
import requests
import random
from getuseragent import UserAgent
from colorama import Fore, init

init(autoreset=True)
ua = UserAgent("android")
useragent = random.choice(ua.list)

accept_languages = [
    "en-US,en;q=0.9",
    "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7"
]
accept_language = random.choice(accept_languages)


def dns_resolver(tg_user_id, proxy=None):
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
        "accept-language": accept_language
    }
    url = 'https://wuffitap-bootstrap-api.wuffi.io/v1/dns-resolver'
    try:
        if proxy is None:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers, proxies=proxy)
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


def farm_tap(dns, access_token, tg_user_id, taps, start_time, end_time, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": "Bearer " + access_token,
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
        "accept-language": accept_language
    }
    url = f'https://{dns}/v1/protected-api/tap'
    data_json = json.dumps(
        {
            "taps": taps,
            "startTime": start_time,
            "endTime": end_time
        }
    )
    try:
        if proxy is None:
            response = requests.put(url, headers=headers, data=data_json)
        else:
            response = requests.put(url, headers=headers, data=data_json, proxies=proxy)
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


def user_login(dns, query, tg_user_id, proxy=None, access_token=None):
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
        "accept-language": accept_language
    }
    if access_token is not None:
        headers['authorization'] = "Bearer " + access_token
    url = f'https://{dns}/v1/public-api/login-telegram'
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
    except requests.RequestException as req_err:
        print(f"{Fore.RED}Ошибка запроса: {req_err}")
        return None
    except Exception as ex:
        print(f"{Fore.RED}Неизвестная ошибка: {ex}")
        return None


def claim_bot(dns, tg_user_id, access_token, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "telegram-user-id": tg_user_id,
        "authorization": "Bearer " + access_token,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": accept_language
    }
    url = f'https://{dns}/v1/protected-api/buff/claim-bot'
    try:
        if proxy is None:
            response = requests.post(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, proxies=proxy)
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


def estimate_earned(dns, tg_user_id, access_token, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "telegram-user-id": tg_user_id,
        "authorization": "Bearer " + access_token,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": accept_language
    }
    url = f'https://{dns}/v1/protected-api/buff/bot/estimate-earned'
    try:
        if proxy is None:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers, proxies=proxy)
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


def tap_status(dns, tg_user_id, access_token, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "telegram-user-id": tg_user_id,
        "authorization": "Bearer " + access_token,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": accept_language
    }
    url = f'https://{dns}/v1/protected-api/tap-status'
    try:
        if proxy is None:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers, proxies=proxy)
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


def tap_config(dns, tg_user_id, access_token, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "telegram-user-id": tg_user_id,
        "Authorization": "Bearer " + access_token,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": accept_language
    }
    url = f'https://{dns}/v1/protected-api/tap-config'
    try:
        if proxy is None:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers, proxies=proxy)
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


def buff(dns, tg_user_id, access_token, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "telegram-user-id": tg_user_id,
        "authorization": "Bearer " + access_token,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": accept_language
    }
    url = f'https://{dns}/v1/protected-api/buff'
    try:
        if proxy is None:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers, proxies=proxy)
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


def using_buff(dns, number_buff, tg_user_id, access_token, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "telegram-user-id": tg_user_id,
        "authorization": "Bearer " + access_token,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": accept_language
    }
    url = f'https://{dns}/v1/protected-api/buff/2/{number_buff}'
    try:
        if proxy is None:
            response = requests.post(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, proxies=proxy)
        return response.json()
    except json.JSONDecodeError as j:
        print(f"{Fore.RED}Ошибка при декодировании JSON ответа: {j}")
        return None
    except requests.RequestException as req_err:
        print(f"{Fore.RED}Ошибка запроса: {req_err}")
        return None
    except Exception as ex:
        print(f"{Fore.RED}Неизвестная ошибка: {ex}")
        return None


def daily_checkin(dns, tg_user_id, access_token, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "telegram-user-id": tg_user_id,
        "authorization": "Bearer " + access_token,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": accept_language
    }
    url = f'https://{dns}/v1/protected-api/user/quests?type=daily_checkin'
    try:
        if proxy is None:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers, proxies=proxy)
        return response.json(), response.status_code
    except json.JSONDecodeError as j:
        print(f"{Fore.RED}Ошибка при декодировании JSON ответа: {j}")
        return None, -1
    except requests.RequestException as req_err:
        print(f"{Fore.RED}Ошибка запроса: {req_err}")
        return None, -1
    except Exception as ex:
        print(f"{Fore.RED}Неизвестная ошибка: {ex}")
        return None, -1


def daily_claim(dns, tg_user_id, task_id, access_token, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "telegram-user-id": tg_user_id,
        "authorization": "Bearer " + access_token,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": accept_language
    }
    url = f'https://{dns}/v1/protected-api/user/quests/claim'
    payload = json.dumps(
        {
            "taskId": task_id
        }
    )
    try:
        if proxy is None:
            response = requests.post(url, headers=headers, data=payload)
        else:
            response = requests.post(url, headers=headers, data=payload, proxies=proxy)
        return response.json(), response.status_code
    except json.JSONDecodeError as j:
        print(f"{Fore.RED}Ошибка при декодировании JSON ответа: {j}")
        return None, -1
    except requests.RequestException as req_err:
        print(f"{Fore.RED}Ошибка запроса: {req_err}")
        return None, -1
    except Exception as ex:
        print(f"{Fore.RED}Неизвестная ошибка: {ex}")
        return None, -1


def activate_tapbot(dns, tg_user_id, access_token, proxy=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "telegram-user-id": tg_user_id,
        "authorization": "Bearer " + access_token,
        "user-agent": useragent,
        "content-type": "application/json",
        "origin": "https://wuffitap.wuffi.io",
        "x-requested-with": "org.telegram.messenger.web",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://wuffitap.wuffi.io/",
        "accept-encoding": "gzip, deflate",
        "accept-language": accept_language
    }
    url = f'https://{dns}/v1/protected-api/buff/'
    payload = json.dumps(
        {
            "botId": "1"
        }
    )
    try:
        if proxy is None:
            response = requests.post(url, headers=headers, data=payload)
        else:
            response = requests.post(url, headers=headers, data=payload, proxies=proxy)
        return response.json(), response.status_code
    except json.JSONDecodeError as j:
        print(f"{Fore.RED}Ошибка при декодировании JSON ответа: {j}")
        return None, -1
    except requests.RequestException as req_err:
        print(f"{Fore.RED}Ошибка запроса: {req_err}")
        return None, -1
    except Exception as ex:
        print(f"{Fore.RED}Неизвестная ошибка: {ex}")
        return None, -1
