import os
import time
import sys
import re
import json
import requests
import signal
from urllib.parse import unquote
from pyfiglet import Figlet
from colorama import Fore
from onlylog import Log

api = "https://fintopio-tg.fintopio.com/api"
header = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://fintopio-tg.fintopio.com/",
    "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    "Webapp": "true"
}

def signal_handler(sig, frame):
    print('Exiting gracefully...')
    sys.exit(0)

def banner():
    os.system("title FINTOPIO BOT" if os.name == "nt" else "clear")
    os.system("cls" if os.name == "nt" else "clear")
    custom_fig = Figlet(font='slant')
    print('')
    print(custom_fig.renderText(' FINTOPIO'))
    print(Fore.RED + '[#] [C] N E T V A L I D X    ' + Fore.GREEN + '[FINTOPIO BOT] $$ ' + Fore.RESET)
    print(Fore.GREEN + '[#] Sambil Ngopi', Fore.RESET)
    print(Fore.YELLOW + '[#] Having Troubles? PM Telegram [t.me/monstabayak] ', Fore.RESET)
    print('')

def runforeva():
    with open('quentod.txt', 'r') as file:
        queryh = file.read().splitlines()
    try:
        value = True
        while value:
            for index, query_id in enumerate(queryh, start=1):
                getname(query_id)
                postrequest(getlogin(query_id))
    except Exception as e:
        Log.error(f'[MAIN] error {e}, restarting')
        runforeva()

def getlogin(querybro):
    try:
        url = api + "/auth/telegram?"
        s = requests.Session()
        s.headers.update({"Webapp": "true"})
        response = s.get(url + querybro, headers=header)
        jData = response.json()
        jsontoken = jData['token']
        Log.success('Login success')
        return jsontoken
    except Exception as e:
        Log.error(f'[getlogin] error {e}')

def getname(querybro):
    try:
        found = re.search('user=([^&]*)', querybro).group(1)
        decodedUserPart = unquote(found)
        userObj = json.loads(decodedUserPart)
        Log.success('username : @' + userObj['username'])
    except Exception as e:
        Log.error(f'[decodedUserPart] error {e}')

def checkin(tomket):
    try:
        url = api + "/daily-checkins"
        s = requests.Session()
        s.headers.update({"Authorization": "Bearer " + tomket})
        response = s.get(url, headers=header)
        jData = response.json()
        Log.warn('reward daily : ' + str(jData['dailyReward']))
        Log.warn('total login day :' + str(jData['totalDays']))
        Log.success('daily reward claimed!')
    except Exception as e:
        Log.error(f'[checkin] failed {e}, restarting')

def nuke(tomket, id, reward):
    try:
        url = api + "/clicker/diamond/complete"
        s = requests.Session()
        s.headers.update({"Authorization": "Bearer " + tomket, "Webapp": "true"})
        textpayload = {"diamondNumber": id}
        response = s.post(url, headers=header, json=textpayload)
        if response.status_code != 200:
            Log.error('[asteroid] failed to claim')
        Log.success('asteroid was crushed!')
        Log.warn('reward : ' + reward)
    except Exception as e:
        Log.error(f'[asteroid] failed {e}, restarting')

def tanamtanamubi(tomket):
    try:
        url = api + "/farming/farm"
        s = requests.Session()
        s.headers.update({"Authorization": "Bearer " + tomket, "Webapp": "true"})
        response = s.post(url, headers=header)
        if response.status_code != 200:
            Log.error('[asteroid] failed to claim')
        Log.success('farming started!')
    except Exception as e:
        Log.error(f'[farming] failed {e} to start')

def panenbrow(tomket):
    try:
        url = api + "/farming/claim"
        s = requests.Session()
        s.headers.update({"Authorization": "Bearer " + tomket, "Webapp": "true"})
        are = s.post(url, headers=header)
        Log.success('farming claimed!')
    except Exception as e:
        Log.error(f'[farming] failed {e} to claim')

def sleep(num):
    for i in range(num):
        print("wait {} seconds".format(num - i), end='\r')
        time.sleep(1)

def postrequest(bearer):
    urldata = '/referrals/data'
    urldiamondstate = '/clicker/diamond/state'
    urlfarmstate = '/farming/state'

    s = requests.Session()
    s.headers.update({"Authorization": "Bearer " + bearer})

    try:
        r = s.get(api + urldata, headers=header)
        jData = r.json()
        jsondaily = jData['isDailyRewardClaimed']
        if not jsondaily:
            Log.warn('daily reward not claimed yet')
            Log.warn('claiming..')
            checkin(bearer)
        Log.warn('balance : ' + jData['balance'])

    except Exception as e:
        Log.error(f'[daily] error {e}, restarting')
        time.sleep(5)
        runforeva()

    try:
        r2 = s.get(api + urldiamondstate, headers=header)
        jData = r2.json()
        jsonsettings = jData['settings']
        jsonstate = jData['state']
        jsondiamondid = jData['diamondNumber']
        jsontotalreward = jsonsettings['totalReward']
        if jsonstate == 'available':
            nuke(bearer, jsondiamondid, jsontotalreward)
        elif jsonstate == 'unavailable':
            Log.warn('asteroid unavailable yet!')
        else:
            Log.warn('asteroid crushed! waiting next round..')

    except Exception as e:
        Log.error(f'[asteroid] error {e}, restarting')
        time.sleep(5)
        runforeva()

    try:
        r3 = s.get(api + urlfarmstate, headers=header)
        jData = r3.json()
        jsonstate = jData['state']
        if jsonstate == 'idling':
            tanamtanamubi(bearer)
        elif jsonstate == 'farming':
            Log.warn('farming not finished yet!')
        elif jsonstate == 'farmed':
            panenbrow(bearer)
        else:
            Log.error('[farming] error')
        print('=========================================')
        sleep(3)

    except Exception as e:
        Log.error(f'[farming] error {e}, restarting')
        time.sleep(5)
        runforeva()

# Menambahkan handler sinyal untuk Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Program utama
if __name__ == "__main__":
    try:
        banner()
        runforeva()
    except KeyboardInterrupt:
        print("Program terminated by user.")
        sys.exit(0)

