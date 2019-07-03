#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
import urllib.request

from colorama import (
    Fore,
    Style
)

from hashlib import md5
from typing import Dict
from getpass import getpass
from bs4 import BeautifulSoup



def get_name(token: str) -> str:
    request = requests.get(f"https://graph.facebook.com/me?access_token={token}")
    return '-'.join(json.loads(request.text)["name"].split(' '))

def dump_profile(token: str):
    if not token:
        print(f"[*] {Fore.RED}YOU NEED TO LOGIN FOR THIS FUNCTIONALITY !{Style.RESET_ALL}")
        return -1
    id = int(input("\n[?] ID of the profile to dump: "))
    request = requests.get(f"https://graph.facebook.com/{id}?access_token={token}")
    data = json.loads(request.text)
    print(f"\n\n\n{data}\n\n\n")


def get_friend(token: str):
    if not token:
        print(f"[*] {Fore.RED}YOU NEED TO LOGIN FOR THIS FUNCTIONALITY !{Style.RESET_ALL}")
        return -1

    request = requests.get(f"https://graph.facebook.com/me/friends?access_token={token}")
    data = json.loads(request.text)
    datas = []
    for friend in data["data"]:
        request = requests.get(f"https://graph.facebook.com/{friend['id']}?access_token={token}")
        data = json.loads(request.text)
        datas.append(f"{str(data)}\n\n\n")
        print(data["name"])

    if not os.path.isdir("output"):
        os.mkdir("output")

    with open(os.path.join("output", f"{get_name(token)}-friend.txt"), 'w') as file:
        file.writelines(datas)

    print(f"Saved on {os.path.join('output', f'{get_name(token)}-friend.txt')}")


def get_token(username: str, password: str):
    # === NUMBERS FROM https://github.com/CiKu370/OSIF ===
    SECRET_KEY = "62f8ce9f74b12f84c123cc23437a4a32"
    API_KEY = "882a8490361da98702bf97a021ddc14d"
    # ====================================================

    sig = f"api_key={API_KEY}credentials_type=passwordemail={username}format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword={password}return_ssl_resources=0v=1.0{SECRET_KEY}"
    data = {
        "api_key": API_KEY,
        "credentials_type":"password",
        "email": username,
        "format": "JSON",
        "generate_machine_id": "1",
        "generate_session_cookies":"1",
        "locale":"en_US",
        "method":"auth.login",
        "password":password,
        "return_ssl_resources":"0",
        "v":"1.0",
        "sig": md5(sig.encode()).hexdigest()
    }



    request = requests.get("https://api.facebook.com/restserver.php", params=data)
    json_data = json.loads(request.text)
    return json_data['access_token']

def create_token(token: str) -> str:
    if token:
        print(f"[*] {Fore.RED}WARNING{Style.RESET_ALL} : A token is already registered")
        ask = input("[?] Are you sure to continue ? [y/N] ")
        if not ask or ask == "n":
            return token

    print(f"\n[!]{Fore.RED} PLEASE NOT THAT I DO NOT STEAL YOUR PASSWORD{Style.RESET_ALL}")
    print("[!] Read the code if you don't believe me ;)")
    username = input("[?] Username: ")
    password = getpass(prompt="[?] Password: ")
    token = get_token(username, password)

    with open(".token", "w") as token_file:
        token_file.write(token)



def asciiArt(logged: bool):
    # Ascii art found here: https://asciiart.website/joan/www.geocities.com/SoHo/7373/crtoon2.html
    print(f"""
                             .--.            .--.
                            ( (`\\\\.\"--``--\".//`) )
                             '-.   __   __    .-'
                              /   /__\\ /__\\   \\
                             |    \\ 0/ \\ 0/    |
                             \\     `/   \\`     /
                              `-.  /-\"\"\"-\\  .-`           ._-.
                                /  '.___.'  \\            //';\\\\
                                \\     I     /           //  ;//
                                 `;--'`'--;`            \\\\_;//
                                   '.___.'               //-`
                                  ___| |___           .\"`-.
                               .-`  .---.  `-.       /     )
                              /   .'     '.   \\     /      )
                             /  /||       ||\\  \\   /  /`\"\"`
                            /  / ||       || \\  \\ /  /
                           /  /  ||       ||  \\  /  /
                          /  (___||___.-=--.   \\   /
                         (                -;    '-'
                          `-----------.___~;

                                Advanced OSIF
                                  {"Logged In" if logged else ""}
                                   0v3rl0w
          """)


if __name__ == "__main__":
    os.system("clear")
    logged = False
    if os.path.isfile(".token"):
        with open(".token", 'r') as token_file:
            logged = True
            token = token_file.read()
    else:
        token = ""

    asciiArt(logged)
    while True:
        user_input = input(">> ")

        if user_input.lower() == "login":
            token = create_token(token)
            exit()

        if user_input.lower() == "dump_friend":
            get_friend(token)

        if user_input.lower() == "dump_profile":
            dump_profile(token)

        if user_input.lower() == "help":
            print("\tlogin\t\t\tGet your infos")
            print("\tdump_friend\t\tDump all your friend's info")
            print("\tdump_profile\t\tDump someone's info with their ID")
