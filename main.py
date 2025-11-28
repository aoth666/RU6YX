import requests
import time
import itertools
import re
from colorama import Fore, Style
import os

RED = Fore.RED
GREEN = Fore.GREEN
BLUE = Fore.BLUE
LRED = Fore.LIGHTRED_EX
LGREEN = Fore.LIGHTGREEN_EX
LBLUE = Fore.LIGHTBLUE_EX
RSET = Style.RESET_ALL

logo = """
██████╗ ██╗   ██╗ █████╗ ██╗   ██╗██╗  ██╗
██╔══██╗██║   ██║██╔═══╝ ╚██╗ ██╔╝╚██╗██╔╝
██████╔╝██║   ██║██████╗  ╚████╔╝  ╚███╔╝
██╔══██╗██║   ██║██╔══██╗  ╚██╔╝   ██╔██╗
██   ██║╚██████╔╝╚█████╔╝   ██║   ██╔╝╚██╗
╚═╝  ╚═╝ ╚═════╝  ╚════╝    ╚═╝   ╚═╝  ╚═╝
"""
os.system("clear")

def main_menu():
    os.system("clear")
    print(LRED + logo + RSET)
    print(LRED + "> Made by kyoja" + RSET)
    print(LRED + "> https://discord.gg/hH8bCNjfSq " + RSET)
    print(LRED + "\n[00] Exit" + RSET)
    print(LRED + "[01] Spam" + RSET)
    print(LRED + "[02] Group Rename" + RSET)
    print()
    return input(LRED + "Choose: " + LGREEN).strip()

def spam(TOKEN, CHANNEL_ID):
    os.system("clear")
    print(LRED + "[!] Edit mentions.txt and messages.txt" + RSET)

    with open("messages.txt", "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    with open("mentions.txt", "r", encoding="utf-8") as f:
        mentions = [line.strip() for line in f if line.strip()]

    mention_text = " ".join([f"<@{user_id}>" for user_id in mentions])

    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
    headers = {"Authorization": TOKEN, "Content-Type": "application/json"}

    print("[!] Started. Press CTRL + C to return to menu.")

    try:
        while True:
            for message_content in messages:
                final_message = f"{message_content} {mention_text}" if mention_text else message_content
                data = {"content": final_message}
                response = requests.post(url, headers=headers, json=data)
                if response.status_code in (200, 201):
                    print(Fore.LIGHTRED_EX + "[+] Sent to " + Fore.LIGHTGREEN_EX + f"{CHANNEL_ID}")
                time.sleep(0)
    except KeyboardInterrupt:
        print(Fore.LIGHTGREEN_EX + "\n[!] Returning to menu..." + RSET)

def group_rename(TOKEN, CHANNEL_ID):
    DELAY = 1

    def get_names():
        names = []
        print(LRED + "Enter names (Type 'end' to finish)" + RSET)
        while True:
            name = input(LRED + "Enter name: " + LGREEN).strip()
            if name.lower() == "end":
                if len(names) < 2:
                    print("Need at least 2 names")
                    continue
                break
            if name:
                names.append(name[:100])
                print("[+] Added name")
        return names

    NAMES = get_names()

    def clean(s):
        return re.sub(r"[\u00A0\x00-\x1F\x7F-\x9F]", " ", s).strip()

    url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}"
    headers = {"Authorization": TOKEN, "Content-Type": "application/json"}

    print(Fore.LIGHTRED_EX + "[*] Started. Press CTRL + C to return to menu." + RSET)

    try:
        for nm in itertools.cycle(NAMES):
            nm = clean(nm)
            try:
                r = requests.patch(url, headers=headers, json={"name": nm}, timeout=10)
            except Exception as e:
                print(Fore.LIGHTBLUE_EX + "[!] Network error." + RSET, e)
                time.sleep(DELAY)
                continue

            if r.status_code == 200:
                print(Fore.LIGHTRED_EX + "[+] Changed to:" + RSET, nm)
                time.sleep(DELAY)
    except KeyboardInterrupt:
        print(Fore.LIGHTGREEN_EX + "\n[*] Returning to menu..." + RSET)

def main():
    TOKEN = input(LRED + "Token: " + LGREEN)
    CHANNEL_ID = input(LRED + "Group ID: " + LGREEN)

    while True:
        choice = main_menu()
        if choice in ["00", "0"]:
            print(LRED + "Exiting..." + RSET)
            break
        elif choice in ["01", "1"]:
            spam(TOKEN, CHANNEL_ID)
        elif choice in ["02", "2"]:
            group_rename(TOKEN, CHANNEL_ID)
        else:
            print(LRED + "[!] Invalid choice." + RSET)
            time.sleep(1)

if __name__ == "__main__":
    main()
