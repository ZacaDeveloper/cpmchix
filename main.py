#!/usr/bin/python

import random
import urllib.parse
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import pystyle
from pystyle import Colors, Colorate

from carparktool import CarParkTool

__CHANNEL_USERNAME__ = "Mister_Dlzz"


def signal_handler(sig, frame):
    print("\n Bye Bye...")
    sys.exit(0)


def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)  # Ensure the index is within bounds
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')
    brand_name =  "Подпишитесь на канал: t.me/CarParkingDizz_Tool"
    colors = [
        "rgb(255,0,0)", "rgb(255,69,0)", "rgb(255,140,0)", "rgb(255,215,0)", "rgb(173,255,47)", 
        "rgb(0,255,0)", "rgb(0,255,255)", "rgb(0,191,255)", "rgb(0,0,255)", "rgb(139,0,255)",
        "rgb(255,0,255)"
    ]
    colorful_text = gradient_text(brand_name, colors)
    console.print(colorful_text)
    print(Colorate.Horizontal(Colors.rainbow, '============================================================'))
    print(Colorate.Horizontal(Colors.rainbow, '\t         Пожалуйста, войдите в CPM перед использованием этого инструмента'))
    print(Colorate.Horizontal(Colors.rainbow, '    Совместное использование ключа доступа запрещено и будет заблокировано'))
    print(Colorate.Horizontal(Colors.rainbow, '                Telegram - Владелец: @Mister_Dlzz'))
    print(Colorate.Horizontal(Colors.rainbow, '                Telegram - Разработик: @ChixNode'))
    print(Colorate.Horizontal(Colors.rainbow, '============================================================'))


def load_player_data(cpm):
    response = cpm.get_player_data()

    if response.get("ok"):
        data = response.get("data")

        if 'floats' in data and 'localID' in data and 'money' in data and 'coin' in data:
        
            print(Colorate.Horizontal(Colors.rainbow, '==========[ ИНФОРМАЦИЯ ОБ ИГРОКЕ ]=========='))
            
            print(Colorate.Horizontal(Colors.rainbow, f'Ник   : {(data.get("Name") if "Name" in data else "UNDEFINED")}.'))
                
            print(Colorate.Horizontal(Colors.rainbow, f'LocalID: {data.get("localID")}.'))
            
            print(Colorate.Horizontal(Colors.rainbow, f'Деньги  : {data.get("money")}.'))
            
            print(Colorate.Horizontal(Colors.rainbow, f'Монет  : {data.get("coin")}.'))
            
        else:
            print(Colorate.Horizontal(Colors.rainbow, '! ERROR: новые учетные записи должны быть зарегистрированы в игре хотя бы один раз!.'))
            exit(1)
    else:
        print(Colorate.Horizontal(Colors.rainbow, '! ERROR: seems like your login is not properly set !.'))
        exit(1)


def load_key_data(cpm):

    data = cpm.get_key_data()

    print(Colorate.Horizontal(Colors.rainbow, '========[ ИНФОРМАЦИЯ О КЛЮЧЕ ]========'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'Ключ : {data.get("access_key")}.'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'Телеграмм ID: {data.get("telegram_id")}.'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'Баланс $  : {(data.get("coins") if not data.get("is_unlimited") else "Unlimited")}.'))


def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            console.print(
                f"[bold red]{tag} cannot be empty or just spaces. Please try again (✘)[/bold red]"
            )
        else:
            return value


def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    print(Colorate.Horizontal(Colors.rainbow, '=============[ ЛОКАЦИЯ ]============='))
    print(Colorate.Horizontal(Colors.rainbow, f'IP Адрес : {data.get("query")}.'))
    print(Colorate.Horizontal(Colors.rainbow, f'Локация   : {data.get("city")} {data.get("regionName")} {data.get("countryCode")}.'))
    print(Colorate.Horizontal(Colors.rainbow, f'Страна    : {data.get("country")} {data.get("zip")}.'))
    print(Colorate.Horizontal(Colors.rainbow, '===================[ МЕНЮ ]==================='))

def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string


if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[bold][1] Введите Email[/bold]", "Email", password=False)
        acc_password = prompt_valid_value("[bold][2] Введите Пароль[/bold]", "Password", password=False)
        acc_access_key = prompt_valid_value("[bold][3] Введите ключ[/bold]", "Access Key", password=False)
        console.print("[bold cyan][%] Попытка вход в систему[/bold cyan]: ", end=None)
        cpm = CarParkTool(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                print(Colorate.Horizontal(Colors.rainbow, 'УЧЕТНАЯ ЗАПИСЬ НЕ НАЙДЕНА.'))
                sleep(2)
                continue
            elif login_response == 101:
                print(Colorate.Horizontal(Colors.rainbow, 'НЕВЕРНЫЙ ПАРОЛЬ.'))
                sleep(2)
                continue
            elif login_response == 103:
                print(Colorate.Horizontal(Colors.rainbow, 'НЕДЕЙСТВИТЕЛЬНЫЙ КЛЮЧ.'))
                sleep(2)
                continue
            else:
                print(Colorate.Horizontal(Colors.rainbow, 'пробовать снова.'))
                print(Colorate.Horizontal(Colors.rainbow, '!Примечание: убедитесь, что вы заполнили все поля!.'))
                sleep(2)
                continue
        else:
            print(Colorate.Horizontal(Colors.rainbow, 'УСПЕШНО'))
            sleep(2)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31" "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45" "46", "47", "48", "49"]
            print(Colorate.Horizontal(Colors.rainbow, '{01}: Увеличить деньги           1.5K'))
            print(Colorate.Horizontal(Colors.rainbow, '{02}: Увеличить монеты           4.5K'))
            print(Colorate.Horizontal(Colors.rainbow, '{03}: Ранг Кинг                  8K'))
            print(Colorate.Horizontal(Colors.rainbow, '{04}: Изменить ID                4.5K'))
            print(Colorate.Horizontal(Colors.rainbow, '{05}: Изменить Имя               100'))
            print(Colorate.Horizontal(Colors.rainbow, '{06}: Изменить Имя (Радуга)      100'))
            print(Colorate.Horizontal(Colors.rainbow, '{07}: Номерные знаки             2K'))
            print(Colorate.Horizontal(Colors.rainbow, '{08}: Удалить аккаунт            FREE'))
            print(Colorate.Horizontal(Colors.rainbow, '{09}: Зарегать аккаунт           FREE'))
            print(Colorate.Horizontal(Colors.rainbow, '{10}: Удалить друзей             500'))
            print(Colorate.Horizontal(Colors.rainbow, '{11}: Разблокировать платные автомобили   5k'))
            print(Colorate.Horizontal(Colors.rainbow, '{12}: Разблокировать все машины           6K'))
            print(Colorate.Horizontal(Colors.rainbow, '{13}: Разблокировать сирену для машин     3.5K'))
            print(Colorate.Horizontal(Colors.rainbow, '{14}: Разблокировать двигетель W16        4K'))
            print(Colorate.Horizontal(Colors.rainbow, '{15}: Разблокировать все гудки            3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{16}: Разблокировать отключение урона     3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{17}: Разблокировать неограниченный бензин  3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{18}: Разблокировать дом 3       4K'))
            print(Colorate.Horizontal(Colors.rainbow, '{19}: Разблокировать дым         4K'))
            print(Colorate.Horizontal(Colors.rainbow, '{20}: Разблокировать колёса      4K'))
            print(Colorate.Horizontal(Colors.rainbow, '{21}: Разблокировать анимации    2K'))
            print(Colorate.Horizontal(Colors.rainbow, '{22}: Разблокировать экипировку (муж)     3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{23}: Разблокировать экипировку (жен)     3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{24}: изменить количество побед в гонках  1K'))
            print(Colorate.Horizontal(Colors.rainbow, '{25}: изменить количество поражений в гонках   1K'))
            print(Colorate.Horizontal(Colors.rainbow, '{26}: Клонировать аккаунт        7K'))
            print(Colorate.Horizontal(Colors.rainbow, '{27}: Пользовательские л.с       2.5K'))
            print(Colorate.Horizontal(Colors.rainbow, '{28}: Пользовательский угол      1.5K'))
            print(Colorate.Horizontal(Colors.rainbow, '{29}: Пользовательские эффект жжения резины    1.5K'))
            print(Colorate.Horizontal(Colors.rainbow, '{30}: Пользовательский пробег автомобиля       1.5K'))
            print(Colorate.Horizontal(Colors.rainbow, '{31}: Пользовательские тормоза автомобиля      2K'))
            print(Colorate.Horizontal(Colors.rainbow, '{32}: Убрать задний бампер       2K'))
            print(Colorate.Horizontal(Colors.rainbow, '{33}: Убрать передний бампер     2K'))
            print(Colorate.Horizontal(Colors.rainbow, '{34}: Изменить пароль от аккаунта   2K'))
            print(Colorate.Horizontal(Colors.rainbow, '{35}: Изменить email аккаунта       2K'))
            print(Colorate.Horizontal(Colors.rainbow, '{36}: Поставить спойлер          10K'))
            print(Colorate.Horizontal(Colors.rainbow, '{37}: Поставить Боди Кит         10K'))
            print(Colorate.Horizontal(Colors.rainbow, '{38}: Разблокировать премиум колёса       4.5K'))
            print(Colorate.Horizontal(Colors.rainbow, '{39}: Разблокировать Toyota Crown         2K'))
            print(Colorate.Horizontal(Colors.rainbow, '{40}: Разблокировать клановскую шапку (М)      3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{41}: Убрать голову (муж)        3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{42}: Убрать голову (жен)          3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{43}: Разблокировать клановский топ 1 (М)      3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{44}: Разблокировать клановский топ 2 (М)      3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{45}: Разблокировать клановский топ 3 (М)      3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{46}: Разблокировать клановский топ 1 (ЖМ)     3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{47}: Разблокировать клановский топ 2 (ЖМ)     3K'))
            print(Colorate.Horizontal(Colors.rainbow, '{48}: Разблокировать Mercedes Cls   4K'))
            print(Colorate.Horizontal(Colors.rainbow, '{49}: Развал Колёс              1K'))
            print(Colorate.Horizontal(Colors.rainbow, '{0} : Exit'))
            
            print(Colorate.Horizontal(Colors.rainbow, '===================[ CPM Chix ]==================='))
            
            service = IntPrompt.ask(f"[bold][?] Select a Service [red][1-{choices[-1]} or 0][/red][/bold]", choices=choices, show_choices=False)
            
            print(Colorate.Horizontal(Colors.rainbow, '===================[ CPM Chix ]==================='))

            if service == 0:  # Exit
                console.print("[bold white] Thank You for using my tool[/bold white]")
            elif service == 1:  # Increase Money
                console.print(
                    "[bold yellow][bold white][?][/bold white] Insert how much money do you want[/bold yellow]"
                )
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Saving your data: ", end=None)
                if amount > 0 and amount <= 500000000:
                    if cpm.set_player_money(amount):
                        console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                        console.print(
                            "[bold green]======================================[/bold green]"
                        )
                        answ = Prompt.ask(
                            "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Thank You for using my tool[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold red]FAILED (✘)[/bold red]")
                        console.print(
                            "[bold red]please try again later! (✘)[/bold red]"
                        )
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED (✘)[/bold red]")
                    console.print("[bold red]please use valid values! (✘)[/bold red]")
                    sleep(2)
                    continue
            elif service == 2:  # Increase Coins
                console.print(
                    "[bold yellow][bold white][?][/bold white] Insert how much coins do you want[/bold yellow]"
                )
                amount = IntPrompt.ask("[?] Amount")
                print("[ % ] Saving your data: ", end="")
                if amount > 0 and amount <= 500000:
                    if cpm.set_player_coins(amount):
                        console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                        console.print(
                            "[bold green]======================================[/bold green]"
                        )
                        answ = Prompt.ask(
                            "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Thank You for using my tool[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold yellow] 'Please use valid values[/bold yellow]"
                    )
                    sleep(2)
                    continue
            elif service == 3:  # King Rank
                console.print(
                    "[bold red][!] Note:[/bold red]: if the king rank doesn't appear in game, close it and open few times.",
                    end=None,
                )
                console.print(
                    "[bold red][!] Note:[/bold red]: please don't do King Rank on same account twice.",
                    end=None,
                )
                sleep(2)
                console.print("[%] Giving you a King Rank: ", end=None)
                if cpm.set_player_rank():
                    console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                    console.print(
                        "[bold yellow] '======================================[/bold yellow]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 4:  # Change ID
                console.print("[bold yellow] '[?] Enter your new ID[/bold yellow]")
                new_id = Prompt.ask("[?] ID")
                console.print("[%] Saving your data: ", end=None)
                if (
                    len(new_id) >= 8
                    and len(new_id)
                    <= 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                    and (" " in new_id) == False
                ):
                    if cpm.set_player_localid(new_id.upper()):
                        console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                        console.print(
                            "[bold yellow] '======================================[/bold yellow]"
                        )
                        answ = Prompt.ask(
                            "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Thank You for using my tool[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold yellow] 'Please use valid ID[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 5:  # Change Name
                console.print("[bold yellow] '[?] Enter your new Name[/bold yellow]")
                new_name = Prompt.ask("[?] Name")
                console.print("[%] Saving your data: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(new_name):
                        console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                        console.print(
                            "[bold yellow] '======================================[/bold yellow]"
                        )
                        answ = Prompt.ask(
                            "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Thank You for using my tool[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold yellow] 'Please use valid values[/bold yellow]"
                    )
                    sleep(2)
                    continue
            elif service == 6:  # Change Name Rainbow
                console.print(
                    "[bold yellow] '[?] Enter your new Rainbow Name[/bold yellow]"
                )
                new_name = Prompt.ask("[?] Name")
                console.print("[%] Saving your data: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(rainbow_gradient_string(new_name)):
                        console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                        console.print(
                            "[bold yellow] '======================================[/bold yellow]"
                        )
                        answ = Prompt.ask(
                            "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Thank You for using my tool[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold yellow] 'Please use valid values[/bold yellow]"
                    )
                    sleep(2)
                    continue
            elif service == 7:  # Number Plates
                console.print("[%] Giving you a Number Plates: ", end=None)
                if cpm.set_player_plates():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 8:  # Account Delete
                console.print(
                    "[bold yellow] '[!] After deleting your account there is no going back !![/bold yellow]"
                )
                answ = Prompt.ask(
                    "[?] Do You want to Delete this Account ?!",
                    choices=["y", "n"],
                    default="n",
                )
                if answ == "y":
                    cpm.delete()
                    console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                    console.print(
                        "[bold yellow] '======================================[/bold yellow]"
                    )
                    console.print(
                        "[bold yellow] f'Thank You for using our tool, please join our telegram channe: @{__CHANNEL_USERNAME__}[/bold yellow]"
                    )
                else:
                    continue
            elif service == 9:  # Account Register
                console.print("[bold yellow] '[!] Registring new Account[/bold yellow]")
                acc2_email = prompt_valid_value(
                    "[?] Account Email", "Email", password=False
                )
                acc2_password = prompt_valid_value(
                    "[?] Account Password", "Password", password=False
                )
                console.print("[%] Creating new Account: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                    console.print(
                        "[bold yellow] '======================================[/bold yellow]"
                    )
                    console.print(
                        "[bold yellow] f'INFO: In order to tweak this account with Telmun[/bold yellow]"
                    )
                    console.print(
                        "[bold yellow] 'you most sign-in to the game using this account[/bold yellow]"
                    )
                    sleep(2)
                    continue
                elif status == 105:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold yellow] 'This email is already exists ![/bold yellow]"
                    )
                    sleep(2)
                    continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 10:  # Delete Friends
                console.print("[%] Deleting your Friends: ", end=None)
                if cpm.delete_player_friends():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 11:  # Unlock All Lamborghinis
                console.print(
                    "[!] Note: this function takes a while to complete, please don't cancel.",
                    end=None,
                )
                console.print("[%] Unlocking All Lamborghinis: ", end=None)
                if cpm.unlock_all_lamborghinis():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 12:  # Unlock All Cars
                console.print("[%] Unlocking All Cars: ", end=None)
                if cpm.unlock_all_cars():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 13:  # Unlock All Cars Siren
                console.print("[%] Unlocking All Cars Siren: ", end=None)
                if cpm.unlock_all_cars_siren():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 14:  # Unlock w16 Engine
                console.print("[%] Unlocking w16 Engine: ", end=None)
                if cpm.unlock_w16():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 15:  # Unlock All Horns
                console.print("[%] Unlocking All Horns: ", end=None)
                if cpm.unlock_horns():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 16:  # Disable Engine Damage
                console.print("[%] Unlocking Disable Damage: ", end=None)
                if cpm.disable_engine_damage():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 17:  # Unlimited Fuel
                console.print("[%] Unlocking Unlimited Fuel: ", end=None)
                if cpm.unlimited_fuel():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 18:  # Unlock House 3
                console.print("[%] Unlocking House 3: ", end=None)
                if cpm.unlock_houses():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 19:  # Unlock Smoke
                console.print("[%] Unlocking Smoke: ", end=None)
                if cpm.unlock_smoke():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 20:  # Unlock Smoke
                console.print("[%] Unlocking Wheels: ", end=None)
                if cpm.unlock_wheels():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(8)
                    continue
            elif service == 21:  # Unlock Smoke
                console.print("[%] Unlocking Animations: ", end=None)
                if cpm.unlock_animations():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 22:  # Unlock Smoke
                console.print("[%] Unlocking Equipaments Male: ", end=None)
                if cpm.unlock_equipments_male():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 23:  # Unlock Smoke
                console.print("[%] Unlocking Equipaments Female: ", end=None)
                if cpm.unlock_equipments_female():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 24:  # Change Races Wins
                console.print(
                    "[bold yellow] '[!] Insert how much races you win[/bold yellow]"
                )
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Changing your data: ", end=None)
                if (
                    amount > 0
                    and amount
                    <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                ):
                    if cpm.set_player_wins(amount):
                        console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                        console.print(
                            "[bold yellow] '======================================[/bold yellow]"
                        )
                        answ = Prompt.ask(
                            "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Thank You for using my tool[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold yellow] '[!] Please use valid values[/bold yellow]"
                    )
                    sleep(2)
                    continue
            elif service == 25:  # Change Races Loses
                console.print(
                    "[bold yellow] '[!] Insert how much races you lose[/bold yellow]"
                )
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Changing your data: ", end=None)
                if (
                    amount > 0
                    and amount
                    <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                ):
                    if cpm.set_player_loses(amount):
                        console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                        console.print(
                            "[bold yellow] '======================================[/bold yellow]"
                        )
                        answ = Prompt.ask(
                            "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Thank You for using my tool[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print(
                            "[bold yellow] '[!] Please use valid values[/bold yellow]"
                        )
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold yellow] '[!] Please use valid values[/bold yellow]"
                    )
                    sleep(2)
                    continue
            elif service == 26:  # Clone Account
                console.print(
                    "[bold yellow] '[!] Please Enter Account Detalis[/bold yellow]"
                )
                to_email = prompt_valid_value(
                    "[?] Account Email", "Email", password=False
                )
                to_password = prompt_valid_value(
                    "[?] Account Password", "Password", password=False
                )
                console.print("[%] Cloning your account: ", end=None)
                if cpm.account_clone(to_email, to_password):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold yellow] '[!] THAT RECIEVER ACCOUNT IS GMAIL PASSWORD IS NOT VALID OR THAT ACCOUNT IS NOT REGISTERED[/bold yellow]"
                    )
                    sleep(2)
                    continue
            elif service == 27:
                console.print(
                    "[bold yellow][!] Note[/bold yellow]: original speed can not be restored!."
                )
                console.print("[bold yellow][!] Enter Car Details.[/bold yellow]")
                car_id = IntPrompt.ask("[bold][?] Car Id[/bold]")
                new_hp = IntPrompt.ask("[bold][?]Enter New HP[/bold]")
                new_inner_hp = IntPrompt.ask("[bold][?]Enter New Inner Hp[/bold]")
                new_nm = IntPrompt.ask("[bold][?]Enter New NM[/bold]")
                new_torque = IntPrompt.ask("[bold][?]Enter New Torque[/bold]")
                console.print(
                    "[bold yellow][%] Hacking Car Speed[/bold yellow]:", end=None
                )
                if cpm.hack_car_speed(car_id, new_hp, new_inner_hp, new_nm, new_torque):
                    console.print("[bold green]SUCCESFUL (✔)[/bold green]")
                    console.print("================================")
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold yellow] '[!] Please use valid values[/bold yellow]"
                    )
                    sleep(2)
                    continue
            elif service == 28:  # ANGLE
                console.print("[bold yellow] '[!] ENTER CAR DETALIS[/bold yellow]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold yellow] '[!] ENTER STEERING ANGLE[/bold yellow]")
                custom = IntPrompt.ask(
                    "[red][?]﻿ENTER THE AMOUNT OF ANGLE YOU WANT[/red]"
                )
                console.print("[red][%] HACKING CAR ANGLE[/red]: ", end=None)
                if cpm.max_max1(car_id, custom):
                    console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                    answ = Prompt.ask(
                        "[red][?] DO YOU WANT TO EXIT[/red] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 29:  # tire
                console.print("[bold yellow] '[!] ENTER CAR DETALIS[/bold yellow]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold yellow] '[!] ENTER PERCENTAGE[/bold yellow]")
                custom = IntPrompt.ask("[pink][?]﻿ENTER PERCENTAGE TIRES U WANT[/pink]")
                console.print("[red][%] Setting Percentage [/red]: ", end=None)
                if cpm.max_max2(car_id, custom):
                    console.print("[bold yellow] 'SUCCESSFUL[/bold yellow]")
                    answ = Prompt.ask(
                        "[bold green][?] DO YOU WANT TO EXIT[/bold green] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 30:  # Millage
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER NEW MILLAGE![/bold]")
                custom = IntPrompt.ask(
                    "[bold blue][?]﻿ENTER MILLAGE U WANT[/bold blue]"
                )
                console.print(
                    "[bold red][%] Setting Percentage [/bold red]: ", end=None
                )
                if cpm.millage_car(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] DO YOU WANT TO EXIT[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 31:  # Brake
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER NEW BRAKE![/bold]")
                custom = IntPrompt.ask("[bold blue][?]﻿ENTER BRAKE U WANT[/bold blue]")
                console.print("[bold red][%] Setting BRAKE [/bold red]: ", end=None)
                if cpm.brake_car(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] DO YOU WANT TO EXIT[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 32:  # Bumper rear
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print(
                    "[bold red][%] Removing Rear Bumper [/bold red]: ", end=None
                )
                if cpm.rear_bumper(car_id):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] DO YOU WANT TO EXIT[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 33:  # Bumper front
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print(
                    "[bold red][%] Removing Front Bumper [/bold red]: ", end=None
                )
                if cpm.front_bumper(car_id):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] DO YOU WANT TO EXIT[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 75:  # /testin endpoint
                console.print("[bold]ENTER CUSTOM FLOAT DATA[/bold]")
                custom = IntPrompt.ask(
                    "[bold][?] VALUE (e.g. 1 or 0)[/bold]"
                )  # This is the value
                console.print(
                    f"[bold red][%] Setting float key... [/bold red]", end=None
                )
                if cpm.testin(custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] DO YOU WANT TO EXIT[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]PLEASE TRY AGAIN[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 34:
                console.print("[bold]Enter New Password![/bold]")
                new_password = prompt_valid_value(
                    "[bold][?] Account New Password[/bold]", "Password", password=False
                )
                console.print("[bold red][%] Changing Password [/bold red]: ", end=None)
                if cpm.change_password(new_password):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] DO YOU WANT TO EXIT[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white]Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]PLEASE TRY AGAIN[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 36:  # telmunnongodz
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER SPOILER ID![/bold]")
                custom = IntPrompt.ask("[bold blue][?]ENTER NEW SPOILER ID[/bold blue]")
                console.print("[bold red][%] SAVING YOUR DATA [/bold red]: ", end=None)
                if cpm.telmunnongodz(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] DO YOU WANT TO EXIT[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 37:  # telmunnongonz
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER BODYKIT ID![/bold]")
                custom = IntPrompt.ask("[bold blue][?]INSERT BODYKIT ID[/bold blue]")
                console.print("[bold red][%] SAVING YOUR DATA [/bold red]: ", end=None)
                if cpm.telmunnongonz(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] DO YOU WANT TO EXIT[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 49:  # telmunnongonz
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER VALUE FOR STANCE [/bold]")
                custom = IntPrompt.ask("[bold blue][?]INSERT VALUE[/bold blue]")
                console.print("[bold red][%] SAVING YOUR DATA [/bold red]: ", end=None)
                if cpm.incline(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] DO YOU WANT TO EXIT[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 35:
                console.print("[bold]Enter New Email![/bold]")
                new_email = prompt_valid_value(
                    "[bold][?] Account New Email[/bold]", "Email"
                )
                console.print("[bold red][%] Changing Email [/bold red]: ", end=None)
                if cpm.change_email(new_email):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] DO YOU WANT TO EXIT[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white]Thank You for using my tool[/bold white]"
                        )
                    else:
                        break
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]EMAIL IS ALREADY REGISTERED [/bold red]")
                    sleep(4)
            elif service == 38:  # SHITTIN
                console.print("[%] Unlocking Premium Wheels..: ", end=None)
                if cpm.shittin():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 39:  # Unlock toyota crown
                console.print(
                    "[!] Note: this function takes a while to complete, please don't cancel.",
                    end=None,
                )
                console.print("[%] Unlocking Toyota Crown: ", end=None)
                if cpm.unlock_crown():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 40:  # Unlock Hat
                console.print("[%] Unlocking Clan Hat: ", end=None)
                if cpm.unlock_hat_m():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 41:  # remove head male
                console.print("[%] Removing Male head: ", end=None)
                if cpm.rmhm():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 42:  # remove head female
                console.print("[%] Removing Female Head: ", end=None)
                if cpm.rmhfm():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 43:  # Unlock TOPM
                console.print("[%] Unlocking Clan clothes Top 1: ", end=None)
                if cpm.unlock_topm():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 44:  # Unlock TOPMz
                console.print("[%] Unlocking Clan clothes Top 1: ", end=None)
                if cpm.unlock_topmz():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 45:  # Unlock TOPMX
                console.print("[%] Unlocking Clan clothes Top 2: ", end=None)
                if cpm.unlock_topmx():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 46:  # Unlock TOPF
                console.print("[%] Unlocking Clan clothes Top: ", end=None)
                if cpm.unlock_topf():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 47:  # Unlock TOPFZ
                console.print("[%] Unlocking Clan clothes Top 1: ", end=None)
                if cpm.unlock_topfz():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 48:  # Unlock Mercedes Cls
                console.print("[%] Unlocking Mercedes Cls: ", end=None)
                if cpm.unlock_cls():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            else:
                continue
            break
        break
