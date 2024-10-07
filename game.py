# Tuodaan kirjastot
from terminaltexteffects.effects.effect_decrypt import Decrypt
from terminaltexteffects.effects.effect_matrix import Matrix
from terminaltexteffects.effects.effect_burn import Burn
from terminaltexteffects.effects.effect_fireworks import Fireworks
from terminaltexteffects.effects.effect_waves import Waves
from colorama import (Fore, Style)
from just_playback import Playback
from geopy import distance
import os
import mysql.connector
import random

connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='user',
    password='user',
    autocommit=True
)


########################################################################################################################
# FUNKTIOT ALKAA
def check_completed_missions():
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM mission_accomplished WHERE game_id = %s", (player,))
    completed_missions_count = cursor.fetchone()[0]
    return completed_missions_count

def clear_console():
    # For Windows, use 'cls', for Mac/Linux, use 'clear'
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS and Linux
        os.system('clear')

def startScreen():
    # Luodaan Decrypt-efekti alkuruudun animaatiota varten
    effect = Decrypt(alkuanimaatioruutu)
    effect.effect_config.merge = True  # Määritetään, että animaatioiden kehykset sulautuvat yhteen

    # Animaatio toistetaan terminaaliin
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

    tmp = input("Press enter to continue")
    clear_console()

def loseScreen():
    # Luodaan Burn-efekti alkuruudun animaatiota varten
    effect = Burn(havioanimaatioruutu)
    effect.effect_config.merge = True  # Määritetään, että animaatioiden kehykset sulautuvat yhteen

    # Animaatio toistetaan terminaaliin
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

    tmp = input("Press enter to continue...")

    clear_console()

def winScreen():
    # Luodaan Fireworks-efekti voittoruudun animaatiota varten
    effect = Fireworks(voittoanimaatioruutu)

    # Animaatio toistetaan terminaaliin
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

    tmp = input("Press enter to continue...")

    clear_console()

def missionCompletedScreen():
    # Luodaan Fireworks-efekti voittoruudun animaatiota varten
    effect = Waves(voittoanimaatioruutu)

    # Animaatio toistetaan terminaaliin
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

    tmp = input("Press enter to continue...")

    clear_console()

def endScreen():
    # Luodaan Matrix-efekti loppuruudun animaatiota varten
    effect = Matrix(loppuanimaatioruutu)

    # Animaatio toistetaan terminaaliin
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

def calcPrice(icao1, icao2):
    cursor = connection.cursor(buffered=True)
    cursor.execute("select latitude_deg, longitude_deg from airport where ident = %s", (icao1,))
    sijainti1 = cursor.fetchall()
    cursor = connection.cursor(buffered=True)
    cursor.execute("select latitude_deg, longitude_deg from airport where ident = %s", (icao2,))
    sijainti2 = cursor.fetchall()
    hinta = int(distance.distance(sijainti1, sijainti2).km) * 1
    return hinta

def getThreat():
    cursor = connection.cursor()
    cursor.execute("SELECT threat FROM game WHERE id = %s", (player,))
    threat = cursor.fetchone()
    threat = int(threat[0])
    return threat

def raiseThreat(type):
    cursor = connection.cursor()
    cursor.execute("SELECT threat FROM game WHERE id = %s", (player,))
    threat = cursor.fetchone()
    threat = int(threat[0])
    if type == "stay":
        if threat + 1 > 100:
            loseGame(player)
        else:
            cursor.execute("UPDATE game SET threat = threat +1 WHERE id = %s", (player,))
            threatLevel = getThreat()
            print(f"HELPER.PY: Analyzing... Threat index is: {threatLevel}")
            connection.commit()

    if type == "failure":
        if threat + 3 > 100:
            loseGame(player)
        else:
            cursor.execute("UPDATE game SET threat = threat +3 WHERE id = %s", (player,))
            threatLevel = getThreat()
            print(f"HELPER.PY: Analyzing... Threat index is: {threatLevel}")
            connection.commit()

    cursor.close()

def lowerThreat():
    cursor = connection.cursor()
    cursor.execute("SELECT threat FROM game WHERE id = %s", (player,))
    threat = cursor.fetchone()
    threat = int(threat[0])
    if threat - 20 > 0:
        cursor.execute("UPDATE game SET threat = threat - 20 WHERE id = %s", (player,))
        connection.commit()
    else:
        cursor.execute("UPDATE game SET threat = 0 WHERE id = %s", (player,))
        connection.commit()
    cursor.close()

def calcCO2(icao1, icao2):
    cursor = connection.cursor()
    cursor.execute("SELECT latitude_deg, longitude_deg from airport where ident = %s", (icao1,))
    sijainti1 = cursor.fetchall()
    cursor = connection.cursor()
    cursor.execute("SELECT latitude_deg, longitude_deg from airport where ident = %s", (icao2,))
    sijainti2 = cursor.fetchall()
    valimatka = int(distance.distance(sijainti1, sijainti2).km)
    if valimatka < 1500:
        paastot = valimatka * 225
    else:
        paastot = valimatka * 120
    cursor.close()
    return paastot

def pay(multiplier, mission, nextMission):
    cursor = connection.cursor()
    cursor.execute("SELECT game.location FROM game WHERE game.id = %s", (player,))
    location_c = cursor.fetchone()
    current_location = location_c[0]
    cursor.execute("SELECT pay FROM mission WHERE id = %s", (mission,))
    money = cursor.fetchone()
    money = int(money[0])
    money = multiplier * money
    money = money + calcPrice(current_location, airports[nextMission])
    cursor.execute("UPDATE game SET money = money + %s WHERE id = %s", (money, player,))
    connection.commit()
    cursor.close()

def pay2(multiplier, mission):
    cursor = connection.cursor()
    cursor.execute("SELECT pay FROM mission WHERE id = %s", (mission,))
    money = cursor.fetchone()
    money = int(money[0])
    money = multiplier * money
    cursor.execute("UPDATE game SET money = money + %s WHERE id = %s", (money, player,))
    connection.commit()
    cursor.close()

def openWeb(webpage):
    clear_console()
    print(Fore.GREEN)
    # print(Fore.GREEN + websivut[webpage])
    if webpage == "ghostrepo.net":
        input("""
            ||||G H O S T R E P O. N E T|||
            --Index--
            * Home
            * Plans
            * Secret sauce...
            * Blog
            * gfdksd
            * dsjhkfg
            hhdd122453rw
            --.... 
            """)
        input("""
            //gotunow
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GhostRepo</title>
            <style>
                body { background: black; color: #0f0; font-family: monospace; text-align: center; }
                a { color: #0f0; text-decoration: none; }
                a:hover { color: red; }
            </style>
            """)
        input("""
            </head>
            <body>
            <h1>WELCOME TO GHOSTREPO</h1>
            <p>Access Restricted. <a href="#" onclick="hack()">Click to Proceed</a></p>
        
            <script>
                function hack() {
                    alert('System compromised. Data collection initiated.');
                    // Fake malware code simulation
                    console.log('Collecting system data...');
                }
            </script>
            </body>
            """)
    if webpage == "privaracapital.org":
        input("""
            <!DOCTYPE html>
            lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Privara Capital</title>
                <style>
                    body { background: #111; color: #ddd; font-family: monospace; text-align: center; padding-top: 50px; }
                    a { color: #f33; } a:hover { color: #f55; }
                </style>
            </head>
            <body>
    
            """)
        input("""
            <h1>Privara Capital</h1>
            <p>Access restricted. <a href="#" onclick="access()">Click to Proceed</a></p>
            <script>
                function access() {
                    if (prompt("Enter access key:") === "PRIVARA123") {
                        document.body.innerHTML = '<h2>Access Granted</h2><p>Loading assets...</p>';} 
                        else {document.body.innerHTML = '<h2>Access Denied</h2>';
                    }}
            </script>
        </body>
        
        """)
    #print(Fore.GREEN + websivut[webpage])
    tmp = input("Exit: [Enter]")

    clear_console()

def travel_to(icao_target):
    cursor = connection.cursor(buffered=True)

    cursor.execute("SELECT game.location FROM game, airport WHERE game.id = %s", (player,))
    location_c = cursor.fetchone()
    current_location = location_c[0]
    target = icao_target
    travel_price = calcPrice(current_location, target)

    cursor = connection.cursor(buffered=True)
    cursor.execute("select money from game WHERE id = %s", (player,))
    saldo = cursor.fetchall()
    atm_saldo = int(saldo[0][0])
    if travel_price > atm_saldo:
        loseGame(player)

    travel_co2 = calcCO2(current_location, target)
    # update location

    cursor = connection.cursor(buffered=True)
    sql_target = f"UPDATE game SET location = (SELECT ident FROM airport WHERE ident = '{target}'),co2_consumed = co2_consumed+'{travel_co2}' WHERE id ='{player}'"
    cursor.execute(sql_target)
    connection.commit()

    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT game.co2_budget FROM game WHERE game.id = %s", (player,))
    budget_co2 = cursor.fetchone()
    co2_budget = budget_co2[0]
    # print(co2_budget)
    # if travel_co2 > co2_budget: ??? co2_budgetti on liian pieni
    # loseGame()

    # update money
    cursor = connection.cursor(buffered=True)
    sql_money = f"UPDATE game SET money = (money -'{travel_price}') WHERE id ='{player}'"
    cursor.execute(sql_money)
    connection.commit()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT game.money FROM game WHERE game.id = %s", (player,))
    money_left = cursor.fetchone()
    print(f"Money left in the budget: {money_left[0]}©")
    lowerThreat()

def travel_menu(country_code):
    cursor = connection.cursor()
    cursor.execute("SELECT game.location FROM game WHERE game.id = %s", (player,))
    location_c = cursor.fetchone()
    current_location = location_c[0]
    cursor = connection.cursor()
    sql_quest = f"SELECT ident, airport.name FROM airport WHERE iso_country ='{country_code}'AND ident != '{current_location}' AND type='medium_airport' ORDER BY RAND() LIMIT 10"
    cursor.execute(sql_quest)
    airports = cursor.fetchall()
    # print(airports)
    icao = []
    names = []
    prices = []
    co2 = []
    # create lists
    for r in airports:
        icao.append(r[0])
        names.append(r[1])
        prices.append(calcPrice(current_location, r[0]))
        co2.append(calcCO2(current_location, r[0]))

    print(Fore.GREEN)
    # print menu
    print("\nAvailable Airports: \n")
    print(f"{'ICAO':<15}{'Names':<35}{'Price':<15}{'CO2(ppm)':<15}")
    for (a, b, c, d) in zip(icao, names, prices, co2):
        b = b.split()[0]
        print(f"{a:<15}{b:<35}{c:<15}{d:<15}")
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT game.money FROM game WHERE game.id = %s", (player,))
    money_left = cursor.fetchone()
    print(f"Money left in the budget: {money_left[0]}©")
    destination = input("Where do you want to go? Please choose airport code from the list: ")
    # if airport code in airports
    if destination in icao or destination != "":
        travel_to(destination)
    else:
        print("Ok. You want to travel later")
    cursor.close()

def loseGame(player):
    # ENDSCREEN NÄKYMÄ (GAME OVER) FAILURE
    print("GAME OVER")
    playback.stop()
    playback.load_file('orch4.mp3') # Lähde: https://www.findsounds.com/ISAPI/search.dll?keywords=orchestra+hit&keywords=orchestra+hit
    playback.play()
    playback.load_file('bgmusicexample.mp3')
    playback.loop_at_end(True)
    playback.play()
    # Luodaan kursori
    cursor = connection.cursor()
    # Tulostetaan lopullinen CO2 mikä jäi käyttämättä
    # cursor.execute("SELECT game.co2_budget FROM game WHERE game.id = %s", (player,))
    # co2_left = cursor.fetchone()
    # print(f"CO2 left in the budget: {co2_left[0]} ppm")
    # Tulostetaan käytetty CO2. Luultavasti tarpeeton, ellei pelissä saa CO2 bonuksia.
    cursor.execute("SELECT co2_consumed FROM game WHERE id = %s", (player,))
    total_used_co2 = cursor.fetchone()
    print(f"Total used CO2: {total_used_co2[0]} ppm")
    # Tulostetaan jäänyt rahamäärä
    cursor.execute("SELECT money FROM game WHERE id = %s", (player,))
    money_left = cursor.fetchone()
    print(f"Money left in the budget: {money_left[0]}€")
    input("Press enter to continue")

    reset()

    loseScreen()
    # Suljetaan kursori ja yhteys
    cursor.close()

    goBack = input("Press Enter to go back to Main Menu: ")
    if goBack == "":
        pauseMenu()
    return

def winGame(player):
    print(Fore.GREEN)
    # ENDSCREEN NÄKYMÄ (WINSTATE) GREAT SUCCESS!
    print("CONGRATULATIONS FOR WINNING THE GAME!")
    # Luodaan kursori
    cursor = connection.cursor()
    # Tulostetaan lopullinen CO2 mikä jäi käyttämättä
    # cursor.execute("SELECT co2_budget FROM game WHERE id = %s", (player,))
    # co2_left = cursor.fetchone()
    # print(f"CO2 left in the budget: {co2_left[0]} ppm")
    # Tulostetaan käytetty CO2. Luultavasti tarpeeton, ellei pelissä saa CO2 bonuksia.
    cursor.execute("SELECT co2_consumed FROM game WHERE id = %s", (player,))
    total_used_co2 = cursor.fetchone()
    print(f"Total used CO2: {total_used_co2[0]} ppm")
    # Tulostetaan jäänyt rahamäärä
    cursor.execute("SELECT money FROM game WHERE id = %s", (player,))
    money_left = cursor.fetchone()
    print(f"Money left in the budget:{money_left[0]}€")

    reset()

    winScreen()

    # Suljetaan kursori ja yhteys
    cursor.close()

    #print("THANK YOU FOR PLAYING THE GAME!
    # \nCREDITS:\nTim Fabritius
    # \nSvetlana Kekkonen-Mattila
    # \nMikko Laakkonen
    # \nJoni Oksanen
    # \nOuti Salonen")

    goBack = input("Press Enter to go back to Main Menu: ")
    if goBack == "":
        pauseMenu()
    return

# location
def mission_airport(ident):
    cursor = connection.cursor(buffered=True)
    sql_quest = f"SELECT airport.name FROM airport WHERE ident = '{ident}'"
    cursor.execute(sql_quest)
    airport = cursor.fetchall()
    cursor.close()
    return airport[0][0]

def mission_country(maat):
    cursor = connection.cursor(buffered=True)
    sql_quest = f"SELECT name FROM country WHERE iso_country = '{maat}'"
    cursor.execute(sql_quest)
    country = cursor.fetchall()
    cursor.close()
    return country[0][0]

"""
# *** POISTETTU OMINAISUUS ***
# def optionMenu():
#    # VALINTAMENU
#    print("Choose action to proceed:\n1.Hack\n2.Web\n3.Buy\n4.Back to Main Menu ")
#
#    while True:
#        choice = int(input("Enter your choice: "))
#        if choice == 1:
#            if currentMission == True:
#                winScreen()
#                break
#            elif currentMission == False:
#                loseGame()
#                break
#        elif choice == 2:
#            openWeb("null")
#            break
#        elif choice == 3:
#            openShop()
#            break
#        elif choice == 4:
#            pauseMenu()
#            break
#        else:
#            print("Invalid choice")

def openShop():
    print("Kauppa")

"""

def quitGame():
    print("Thank you for playing!")

def reset():
    playerDeleteQuery = print(f"Do you want to delete player {player} [Y/N]?\n ")
    if playerDeleteQuery == "Y" or playerDeleteQuery == "y":
        cursor = connection.cursor()
        cursor.execute("DELETE FROM game WHERE id = %s", (player,))
        cursor.execute("DELETE FROM mission_accomplished WHERE game_id = %s", (player,))
        cursor.close()
    elif playerDeleteQuery == "N" or playerDeleteQuery == "n":
        pauseMenu()

def pauseMenu():
    print(Fore.GREEN)
    print("Pause Menu\n1.Start Game\n2.Delete Player\n3.Quit Game\n ")

    while True:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            init()
            break
        elif choice == 2:
            reset()
            break
        elif choice == 3:
            quitGame()
            break
        else:
            print("Invalid choice")

def init_maat():
    global maat

    cursor = connection.cursor(buffered=True)
    # Maiden arpominen
    countries_sql = "SELECT iso_country FROM country ORDER BY RAND() LIMIT 3"
    cursor.execute(countries_sql)
    countries = cursor.fetchall()

    maat.clear()  # Clear previous values to avoid duplicates or lingering data
    for country in countries:
        maat.append(country[0])

def init_airports():
    global airports
    while len(airports)<3:
        init_maat()

        airports.clear()  # Clear previous values
        cursor = connection.cursor(buffered=True)
        for maa in maat:
            airports_sql = f"SELECT ident FROM airport WHERE iso_country = '{maa}' ORDER BY RAND() LIMIT 1"

            cursor.execute(airports_sql)
            airport = cursor.fetchall()

            # Debug print to see the fetched airport
            print(f"Fetched airport for {maa}: {airport}")

            # Ensure the query returned at least one result
            if airport:
                airports.append(airport[0][0])
            else:
                print(f"No airport found for country: {maa}")

def init():
    # Kysytään pelaajan nimi
    print("HACKING USER ID DATABASE...\nACCESS GRANTED...")
    player = input("USE ALIAS: ")

    init_airports()
    #print(maat)
    #print(airports)
    #input("...")
    cursor = connection.cursor(buffered=True)
    # Tarkistetaan onko annettu pelaaja jo olemassa
    cursor.execute("SELECT COUNT(*) FROM game WHERE id = %s", (player,))
    result = cursor.fetchone()

    if result[0] > 0:
        print(f"Welcome back, {player}!")
    else:
        # Luodaan uusi pelaaja
        cursor.execute("INSERT INTO game(id) VALUES (%s)", (player,))
        connection.commit()
        print(f"Welcome, {player}! Your alias has been created.")

        # Annetaan uudelle pelaajalle sijainti
        cursor.execute("UPDATE game SET location = %s WHERE id = %s", (airports[0], player))
        connection.commit()

        # Annetaan uudelle pelaajalle lähtötiedot
        cursor.execute("UPDATE game SET co2_consumed = %s WHERE id = %s", (0, player))
        cursor.execute("UPDATE game SET co2_budget = %s WHERE id = %s", (1000, player))
        cursor.execute("UPDATE game SET money = %s WHERE id = %s", (1000, player))
        cursor.execute("UPDATE game SET threat = %s WHERE id = %s", (0, player))
        connection.commit()

    # Suljetaan kursori ja yhteys
    cursor.close()

    return player

def mission0():
    print(Fore.GREEN)
    # Mission 0 - Tutorial
    # After playerGreeting
    # mission location/ country
    airport = mission_airport(airports[0])
    country = mission_country(maat[0])
    print(f"* You arrived to {airport} in {country}")
    # Mission scoretracking
    missionScoreMax = 4
    missionScore = 0
    print(Fore.GREEN)
    print("* Later on... ")
    print("______________________________________________________________________________")
    input("HELPER.PY: Standing by. Type anything to initiate ImIn-protocol: ")
    input("Brute accessing domain... 'PhantomGrid'")
    input("Entry aborted: STATUS: Critical program failure")
    print("______________________________________________________________________________")
    input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
    input(f"USER: Gh0stP@cket sent: cool moves '{player}' lmao. (HELPER.PY:[Enter]: (Input whatever to progress)): ")

    joinInput = input(f"User: Gh0stP@cket sent: wanna join? (HELPER.PY: Type yes to join.): ")

    if joinInput == "yes":
        input("USER: Gh0stP@cket sent: sweet, go to ghostrepo.net and check details. (HELPER.PY:[Enter]): ")
    else:
        input("USER: Gh0stP@cket sent: unlucky lol bye (HELPER.PY:[Enter]): ")
        # Ghostpacker infilitrates your pc here.
        input("""
              $ sudo ls /var/log
              access.log  syslog.log  .hidden
              $ sudo cat /var/log/.hidden
              Error: Permission Denied
              $ sudo chmod 777 /var/log/.hidden
              $ sudo cat /var/log/.hidden
              """)
        input("""
              [ROOTKIT] Installing stealth modules...
              [ROOTKIT] Patching kernel hooks...
              [ROOTKIT] Redirecting network traffic to 192.168.1.100...
              [ROOTKIT] Disabling system logging...
              [ROOTKIT] Erasing traces from /var/log/...
              [ROOTKIT] Operation complete. System compromised.
              $ sudo ls /dev/ 
                """)
        input("""
              tty1  tty2  null  zero  backdoor  sd0
              $ ps aux | grep -i backdoor
              root      1337  0.0  0.0  0.0    /usr/lib/backdoor.sh
              $ sudo kill -9 1337
              Error: Process cannot be terminated
              byeAndEat****
              $ echo 'System integrity compromised.'  
              """)

        #Losing game if faulty answer.
        loseGame(player)

    # Player checks given website through the web-tab
    # enterWebUrl("requiredUrl")
    webQuery1 = input("Please enter url: ")
    while True:
        if webQuery1 == "ghostrepo.net":
            openWeb(webQuery1)
            break
        else:
            print("404: Page not found.")
            webQuery1 = input("Please enter url: ")

    input("USER: Gh0stP@cket sent: lol ty (HELPER.PY:[Enter]): ")
    input("""
          $ sudo chmod 777 /var/log/.hidden
          $ sudo cat /var/log/.hidden
          [ROOTKIT] Installing stealth modules...
          [ROOTKIT] Patching kernel hooks...
          [ROOTKIT] Disabling system logging...
          [ROOTKIT] Operation complete. System compromised.
          $ sudo ls /dev/
          """)
    input("""
          tty1  tty2  null  zero  backdoor  sd0
          $ ps aux | grep -i backdoor
          root      1337  0.0  0.0  0.0    /usr/lib/backdoor.sh
          $ sudo kill -9 1337
          Error: Process cannot be terminated
          """)

    input("User: Gh0stP@cket sent: pretty incredible you walked right in that. (HELPER.PY:[Enter]): ")
    input("User: Gh0stP@cket sent: figured you might be bit brighter. (HELPER.PY:[Enter]): ")
    input("User: Gh0stP@cket sent: w/e.\nif you want your encrypted files back without being spread to whoever, "
          "we need some insurance. (HELPER.PY:[Enter]): ")
    input("User: Gh0stP@cket sent: you got in through the backdoor we set up for eager beavers such as you."
          "\ntarget is privara capital. Use your head and get to it.")
    print("______________________________________________________________________________")
    input("HELPER.PY: Check: privaracapital.org on the web. (HELPER.PY:[Enter]): ")

    # Player goes to website - learns more about going to web for info.
    webQuery2 = input("Please enter url: ")
    while True:
        if webQuery2 == "privaracapital.org":
            openWeb(webQuery2)
            break
        else:
            print("404: Page not found. ")
            webQuery2 = input("Please enter url: ")
    # We might need an active message display somewhere after all(?)
    input("HELPER.PY: First, create a new user then infiltrate their crm and internal cashflow.(HELPER.PY:[Enter]): ")

    print("'Welcome to Privara. We care about your assets.' ")

    # Fake bank fake account
    newPrivaraKey = random.randint(1000, 9999)  # Luo satunnaisen 4-numeroisen avaintunnuksen
    print(f"Your 4-digit key id is: {newPrivaraKey}")
    while True:
        newPrivaraPassword = int(input("Please input new password (4 numbers): "))
        if newPrivaraKey == "":
            print("Invalid password. Please, try again. ")
        else:
            break

    print("Password set.")
    print("______________________________________________________________________________")
    input("HELPER.PY: Please take mental note of these credentials. (HELPER.PY:[Enter]): ")

    while True:

        privaraKey = int(input(f"Please input your 4-number id: "))
        privaraPassword = int(input(f"Please input your password: "))
        if privaraPassword == newPrivaraPassword and privaraKey == newPrivaraKey:
            print("Log in successful.")
            break
        else:
            print("Log in failed.")
            input("HELPER.PY: Please try again. (HELPER.PY:[Enter]): ")
            privaraPassword = int(input(f"Please input your password: "))

    print("______________________________________________________________________________")
    input("HELPER.PY:  would you like to do? \n(Enter) Use rootkit ")
    input("Deploying rootkit... ")
    input("$ sudo dmesg | tail")
    input("[13562.33] USB device 3-1: New USB device connected, idVendor=16d0, idProduct=0af2")
    input("[13562.35] USB device 3-1: HID device initialized"
          "\n[13562.37] Rootkit module loaded from /dev/usb/backdoor")
    input("[13562.40] Kernel hook injected at 0xFFFF0A34...")
    input("$ ls /dev/usb/backdoor    rootkit.sh    terminal.txt")

    print("$ sudo cat /dev/usb/rootkit.sh#!/bin/bash")
    print("echo [ROOTKIT] Accessing bank transaction logs..."
          "\nsleep 1")
    print("echo [ROOTKIT] Re-routing transactions to 192.168.1.200..."
          "\nsleep 1")
    print("echo [ROOTKIT] Masking malicious activity in logs..."
          "\nsleep 1")
    print("echo [ROOTKIT] Uploading data to external server...")
    print("""
    $ sudo netstat -an | grep 192.168.1.200
    tcp        0      0 192.168.1.50:45328     192.168.1.200:8080     ESTABLISHED
    $ sudo ps aux | grep rootkit
    root       3137  0.0  0.1  13672  2640 ?        S    10:32   0:00 /dev/usb/rootkit.sh
    root       3151  0.0  0.0   6428  1144 ?        S    10:32   0:00 /usr/lib/backdoor
    """)

    print("$ echo System compromise in progress.")
    print("______________________________________________________________________________")
    # Player will tutorial missions here.
    while True:
        firstTask = input("access_point 20: int2**3*int5\nCaseFalse =? : ")

        if firstTask == "yes" or firstTask == "true":
            print("ERROR: Critical user error. ")
        elif firstTask == "no" or firstTask == "false":
            correctAnswer = int(input("Please input correct variable: "))
            if correctAnswer == 40:
                print("access_point 20: STATUS: GREEN ")
                missionScore = missionScore + 2
                print(f"HELPER.PY: Mission progress: {missionScore} / {missionScoreMax}")
                break
        else:
            print("User error. ")
    print("______________________________________________________________________________")
    while True:
        secondTask = input("system_check 15: 5 * 4?\nCaseFalse =? : ")

        # Käyttäjän vastauksen tarkistus
        if secondTask == "no" or secondTask == "false":
            print("system_check 15: STATUS: GREEN ")
            missionScore = missionScore + 2
            print(f"HELPER.PY: Mission progress: {missionScore} / {missionScoreMax}")
            break

        elif secondTask == "yes" or secondTask == "true":
            print("WARNING: Incorrect response. ")
            correction = input("Please input the correct value: ")

            if correction == 20:
                print("system_check 15: STATUS: GREEN ")
                missionScore = missionScore + 1
                print(f"HELPER.PY: Mission progress: {missionScore} / {missionScoreMax}")
                break
            else:
                print("User error. ")

    print("______________________________________________________________________________")
    # Teach about the threat-mechanic via intrusion
    threatLevel = getThreat()
    print(f"HELPER.PY: Threat index is: {threatLevel}. ")
    print("HELPER.PY: /!\WARNING/!\: Threat-level will indicate you of mission parameters."
          "\nPlease be mindful of this during your work. (HELPER.PY:[Enter]): ")
    # Here is where we update the threat level for the first time.
    print("______________________________________________________________________________")
    # Player goes home
    print("Going home...")
    print("______________________________________________________________________________")
    input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
    input("USER: Gh0stP@cket sent: that did the trick (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: ill vouch for you, welcome aboard newbie. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: t2u theyre going to be sorting through their **** for a while. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: anyway, now thats done. Time to move on to bigger fish. (HELPER.PY:[Enter]): ")
    print("______________________________________________________________________________")
    print(f"(HELPER.PY:[Enter]): Guided mission protocol over. Good luck {player}")
    print(f"HELPER.PY: Mission completed, score: {missionScore} / {missionScoreMax}. Base Pay: 1000©")

    #Clearing the mission
    if missionScore == missionScoreMax:
        scoreModifier = 1.15
        input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
              f"\nPay: {1000*scoreModifier}.")
    elif missionScore < missionScoreMax:
        scoreModifier = 0.75
        input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
              f"\nPay: {1000*scoreModifier}.")
    elif missionScore >= 0:
        scoreModifier = 0.5
        input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
              f"\nPay: {1000*scoreModifier}.")
    else:
        scoreModifier = 0.5
        input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
              f"\nPay: {1000*scoreModifier}.")

    pay(scoreModifier, 0, 1)
    input("HELPER.PY: Mission complete! ")
    missionCompletedScreen()
    #Update mission status
    cursor = connection.cursor(buffered=True)
    print("* Changing location... ")
    travel_menu(maat[0])
    cursor.execute("INSERT INTO mission_accomplished(game_id, mission_id) VALUES (%s, %s)", (player, 0))
    connection.commit()
    cursor.close()
    input("Press enter to continue ")
    clear_console()
    travel_to(airports[1])

def mission1():
    #Mission scoretracking
    missionScoreMax = 11
    missionScore = 0
    print(Fore.GREEN)
    print("Mission 1")
    # mission location/ country
    airport1= mission_airport(airports[1])
    country1 = mission_country(maat[1])
    print(f"* You arrived to {airport1} in {country1}")
    print(Fore.GREEN)
    print("* Later on... ")
    #Description-print here

    input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
    # input("USER: Gh0stP@cket sent:  (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: all set newbie? (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: next on the list: NeuraGenix. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: they got press attention due to some ethical issues "
          "relating to workers and testing procedures. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: not that theyre entirely rotten, they just kinda exist on a bad frontier. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: unlucky however fact however is that theyre being quiet. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: sent ya smth. Should help with biometrics but otherwise its in your hands. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: youre in but youre still on the lookout before we vest in you fully. (HELPER.PY:[Enter]): ")

    #######################################################################################################################
    # Step 1
    step1_1State = 0
    while True:
        if step1_1State == 1:
            breakQuery = input("HELPER.PY: Would you like to move to NeuraGenix? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("HELPER.PY: Moving to target. ")
                break
            elif breakQuery == "no":
                print("______________________________________________________________________________")
                query1_1 = input("HELPER.PY: What would you like to do?"
                                  "\n(1): Check delivery "
                                  "\n(2): Locations "
                                  "\n(3): Web "
                                  "\n(4): Status "
                                  "\n(5): Move "
                                  "\n "
                                  "\nInput: ")
        elif step1_1State == 0:
            print("______________________________________________________________________________")
            query1_1 = input("HELPER.PY: What would you like to do?"
                              "\n(1): Check delivery "
                              "\n(2): Locations "
                              "\n(3): Web "
                              "\n(4): Status "
                              # "\n(5): Move "
                              "\n "
                              "\nInput: ")

        if query1_1 == "1":
            print("HELPER.PY: You were sent a usb-drive. It seems to contain a bypass-program. "
                  "Note inside says: 'Get me in their intra. -KeGh'")
        elif query1_1 == "2":
            if step1_1State == 0:
                # print("HELPER.PY: ")
                print("HELPER.PY: Current available locations are: "
                      "\n>Home<"
                      "\n ")
            elif step1_1State == 1:
                print("HELPER.PY: Current available locations are: "
                      "\n>Home<"
                      "\n*NeuraGenix"
                      "\n ")
        elif query1_1 == "3":
            input("HELPER.PY: Searching web for NeuraGenix home page. [Enter]")
            input("HELPER.PY: Indexing search results. [Enter]")
            input("HELPER.PY: Location data stored. Analyzing route. [Enter]")
            print("HELPER.PY: NeuraGenix added to locations-list.")
            step1_1State = 1
            print("State updated."
                  "\n ")
        elif query1_1 == "4":
            threatLevel = getThreat()
            print(f"HELPER.PY: Analyzing... Threat index is: {threatLevel}")
        elif query1_1 == "5":
            breakQuery = input("HELPER.PY: Would you like to move to NeuraGenix? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("HELPER.PY: Moving to target.")
                break
            elif breakQuery == "no":
                print("______________________________________________________________________________")
                query1_1 = input("HELPER.PY: What would you like to do?"
                                  "\n(1): Check delivery "
                                  "\n(2): Locations "
                                  "\n(3): Web "
                                  "\n(4): Status "
                                  "\n(5): Move "
                                  "\n "
                                  "\nInput: ")

    #######################################################################################################################
    # Step 2
    print("HELPER.PY: Arrived at NeuraGenix headquarters. ")
    step1_2State = 0
    while True:
        if step1_2State == 1:
            breakQuery = input("HELPER.PY: Head inside NeuraGenix? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("HELPER.PY: Entering building. ")
                break
            elif breakQuery == "no":
                print("______________________________________________________________________________")
                query1_2 = input("HELPER.PY: What would you like to do? "
                                   "\n(1): Check surroundings"
                                   "\n(2): Locations "
                                   "\n(3): Status "
                                   "\n(4): Move "
                                   "\n "
                                   "\nInput: ")
        elif step1_2State == 0:
            print("______________________________________________________________________________")
            query1_2 = input("HELPER.PY: What would you like to do? "
                               "\n(1): Check surroundings"
                               "\n(2): Locations "
                               "\n(3): Status "
                               # "\n(4): Move "
                               "\n "
                               "\nInput: ")

        if query1_2 == "1":
            input("HELPER.PY: You are currently outside NeuraGenix. There are guards posted at the front entrance. [Enter]")
            input("HELPER.PY: You will not be able to get in with your current status. [Enter]")
            input("HELPER.PY: There's a cafeteria within the block vicinity. We should head on over and perform a local network-scan. [Enter]")
            print("HELPER.PY: Enroute... Arrived.")
            print("5 minutes after ordering... ")

            while True:
                print("HELPER.PY: System standby. Showing lan-options. ")
                commandExecute = input("HELPER.PY: Execute local network-scan, select desired lan: "
                                       "\n (1) -freeWifi"
                                       "\n (2) -beanWifi"
                                       "\n (3) -visitorWifi"
                                       "\n Input: ")
                if (commandExecute == "1"):
                    input("HELPER.PY: Network scan underway... ")
                    input("HELPER.PY: Package analysis 5/65... ")
                    input("HELPER.PY: Package analysis 17/65... ")
                    input("HELPER.PY: Package analysis 38/65... ")
                    input("HELPER.PY: Package analysis complete. ")
                    input("HELPER.PY: No entry points located. ")
                elif (commandExecute == "2"):
                    input("HELPER.PY: Network scan underway... ")
                    input("HELPER.PY: Package analysis 5/30... ")
                    input("HELPER.PY: Package analysis 15/30... ")
                    input("HELPER.PY: Package analysis complete. ")
                    input("HELPER.PY: No entry points located. ")
                elif (commandExecute == "3"):
                    input("HELPER.PY: Network scan underway... ")
                    input("HELPER.PY: Package analysis 23/125... ")
                    input("HELPER.PY: Package analysis 50/125... ")
                    input("HELPER.PY: Package analysis 105/125... ")
                    input("HELPER.PY: Package analysis 118/125... ")
                    input("HELPER.PY: Package analysis complete. ")
                    input("HELPER.PY: Potential access point discovered. -DeepScan.init")
                    print("HELPER.PY: Disovery analysis: Potential VPN entry weakness ")

                    breakIn = input("Deploy probe? [yes/no]: ")
                    if breakIn == "yes":
                        input(
                            """   
                            echo "[INFO] Initializing connection to target VPN gateway..."
                            sleep 2
                            echo "[INFO] Connecting to DataSec Solutions VPN at 198.51.100.7:443"
                            sleep 3
                            echo "[SUCCESS] VPN connection established. Bypassing authentication... "
                            """)

                        # TASKS HERE
                        addScore = mission1Tasks(missionScore)
                        missionScore+=addScore
                        print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                        threatLevel = getThreat()
                        print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                        #WARNING
                        if threatLevel >= 40:
                            input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                                  "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                        input("""
                        echo "[INFO] Firewall breach alerted."
                        sleep 2
                        echo "[INFO] Break-in protocol underway..."
                        sleep 3
                        echo "[SUCCESS] Firewall disabled."
                        sleep 2
                        echo "[INFO] Overwriting logs..."
                        sleep 2 
                        """)

                        # TASKS HERE
                        addScore = mission1Tasks(missionScore)
                        missionScore += addScore
                        print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                        threatLevel = getThreat()
                        print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                        # WARNING
                        if threatLevel >= 40:
                            input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                                  "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                        input("""
                        echo "[INFO] Executing exploit on CVE-2024-1234 - Authentication Bypass Exploit"
                        sleep 2
                        echo "[INFO] Injecting payload..."
                        sleep 3
                        echo "[SUCCESS] Payload injected successfully. Access granted to internal network. "
                        """)

                        # TASKS HERE
                        addScore = mission1Tasks(missionScore)
                        missionScore += addScore
                        print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                        threatLevel = getThreat()
                        print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                        # WARNING
                        if threatLevel >= 40:
                            input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                                  "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                        input("""
                        echo "[INFO] Scanning internal network for accessible resources..."
                        sleep 2
                        echo "[INFO] Discovered 3 active servers:"
                        sleep 1
                        """)
                        input("""
                        echo "      [1] FileServer01 - 192.168.1.10"
                        echo "      [2] DatabaseServer - 192.168.1.20"
                        echo "      [3] MailServer - 192.168.1.30"
                        """)
                        input("""
                        sleep 1
                        echo "[INFO] Attempting to access DatabaseServer..."
                        sleep 2
                        echo "[INFO] Failure, biometric security detected."
                        sleep 1
                        """)
                        input("""
                        echo "[INFO] Generating id data."
                        sleep 1
                        echo "[SUCCESS] ID data generated."
                        sleep 1
                        """)
                        input("""
                        echo "[SUCCESS] Access id linked with RFID."
                        sleep 1
                        echo "[INFO] Command finished. Quitting program... Cleaning logs... "
                        """)
                        step1_2State = 1
                        print("State updated. "
                              "\n")
                        break
                    else:
                        input("HELPER.PY: Entry-probe disabled. Cleaning logs. ")
        elif query1_2 == "2":
            if step1_2State == 0:
                print("HELPER.PY: Current available locations are: "
                      "\n>NeuraGenix<"
                      "\n ")
            elif step1_2State == 1:
                print("HELPER.PY: Current available locations are: "
                      "\n*NeuraGenix"
                      "\n>Cafeteria<"
                      "\n ")
        elif query1_2 == "3":
            threatLevel = getThreat()
            print(f"HELPER.PY: Analyzing... Threat index is: {threatLevel}")
        elif query1_2 == "4":
            breakQuery = input("HELPER.PY: Head inside NeuraGenix? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("HELPER.PY: Entering building. ")
                break
            elif breakQuery == "no":
                print("______________________________________________________________________________")
                query1_2 = input("HELPER.PY: What would you like to do?"
                                   "\n(1): Check surroundings"
                                   "\n(2): Locations "
                                   "\n(3): Status "
                                   "\n(4): Move "
                                   "\n "
                                   "\nInput: ")

    #######################################################################################################################
    # Step 3
    step1_3State = 0
    while True:
        if step1_3State == 1:
            print ("DEBUG: Mission should be over.")
        elif step1_3State == 0:
            print("You're stopped by the guards. Flashing your RFID-card, you're given access to the premises."
            "\nThough they seem wary, they let you through. You're now within the premises.")
            print("______________________________________________________________________________")
            query1_3 = input("HELPER.PY: What would you like to do? "
                           "\n(1): Check surroundings"
                           "\n(2): Locations "
                           "\n(3): Status "
                           "\n "
                           "\nInput: ")

        if query1_3 == "1":
            print("Before you is a large lobby. You see an info-desk, waiting area with seats and some bathrooms. ")
            print("______________________________________________________________________________")
            moveOption = input("What would you like to do? "
                               "\n (1): Info-desk "
                               "\n (2): Waiting area "
                               "\n (3): Bathroom "
                               "\n Input: ")

            if moveOption == "1":
                input("* Going to the info-desk, you try to chat up the attendant."
                      "\nYou are inquired for your business and contact personnel. ")
                input("* Trying to smooth talk isn't successful. "
                      "\nYou are asked to leave the area before the guards will be alerted.")
                print("HELPER.PY: Critical mission failure.")
                loseGame(player)
                break
            elif moveOption == "2":
                input("* Going to the waiting area, you sit down with a presence. ")
                input("* Waiting a bit, exuding intended presence, you note ignoring other passerby's. ")
                input("* Noting the attendant is busy with transfer calls and paperwork. ")
                input("* You bring out your laptop as if waiting for someone to come pick you up. ")
                input("* You install the usb you were provided. This brings out an remote access panel. ")
                print("______________________________________________________________________________")
                input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
                input("USER: K3rn3lGh0$t sent: HEH gotchu now.  (HELPER.PY: [Enter]) ")
                input("USER: K3rn3lGh0$t sent: Lmao, don't sweat it. We already had your stuff.  (HELPER.PY: [Enter]) ")

                input("USER: K3rn3lGh0$t sent: Anyway, sit back. Don't look stiff, I'll help ya out.  (HELPER.PY: [Enter]) ")
                input("-KGRoot.init .\clientConnection:500.6904-676@LogPoint:6784.1245.3455.000.000:  (HELPER.PY: [Enter]) ")
                input(""" 
                        echo "[INFO] Executing exploit on CVE-2024-1234 - Authentication Bypass Exploit"
                        sleep 2
                        echo "[INFO] Injecting payload..."
                        sleep 3
                        echo "[SUCCESS] Payload injected successfully. Access granted to internal network. "
                        """)
                input(""" 
                        echo "[INFO] Scanning internal network for accessible resources..."
                        sleep 2
                        echo "[INFO] Discovered 3 active servers:"
                        sleep 1
                        """)
                input(""" 
                        echo "      [1] FileServer01 - 192.168.1.10"
                        echo "      [2] DatabaseServer - 192.168.1.20"
                        echo "      [3] MailServer - 192.168.1.30"
                        sleep 1
                        """)
                input("""
                        echo "[INFO] Attempting to access DatabaseServer..."
                        sleep 2
                        echo "[SUCCESS] Secure.server access established. -HANDSHAKE- .kg\ForceOpen.exe."
                    """)

                # TASKS HERE
                addScore = mission1Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input(
                    """
                    // Initializing NeuraGenix Biometric Security Bypass
                    >>> Initializing facial recognition bypass...
                    """)
                input("""
                    [Scanning NeuraGenix executive database...]
                    [Acquiring facial image dataset...]
                    """)
                input("[Generating 3D facial model... 5%]")
                input("[Generating 3D facial model... 12%]")
                input("[Generating 3D facial model... 54%]")
                input("[Generating 3D facial model... 80%]")
                input("[Generating 3D facial model... 90%]")
                input("""
                    >>> Facial recognition match: 97% accuracy
                    >>> Status: Bypass successful
                    """)
                input("""
                    // Proceeding to voiceprint authentication...
                    >>> Initiating voiceprint data extraction...
                     """)

                # TASKS HERE
                addScore = mission1Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("""
                [Accessing archived audio files...]
                [Extracting voice patterns: Frequency, Pitch, Tone...]
                """)
                input("[Generating synthetic voice model...2%]")
                input("[Generating synthetic voice model...5%]")
                input("[Generating synthetic voice model...47%]")
                input("[Generating synthetic voice model...78%]")
                input("[Generating synthetic voice model...87%]")
                input("""
                >>> Voiceprint match: 92% accuracy
                >>> Status: Bypass successful
                 """)

                # TASKS HERE
                addScore = mission1Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("""
                // Biometric authentication completed
                >>> Access granted to secure files
                >>> Navigating to "Nexus_Prototype" folder...
                [Decrypting folder contents...]
                [Data extraction in progress...]
                >>> 45% complete...
                >>> 80% complete...
                >>> 100% complete!
                >>> Project Nexus data successfully extracted.
                >>> Warning: Security systems triggered. Initiating escape protocol...
                 """)
                print("______________________________________________________________________________")
                input("USER: K3rn3lGh0$t sent: Done, got the packet. Rest is on you. (HELPER.PY: [Enter]) ")
                print("______________________________________________________________________________")
                input("HELPER.PY: It would be reasonable to exit the premises. You have however raised suspicion. [Enter]")
                input("HELPER.PY: Your details have been presumably caught by the security cameras. [Enter]")
                input("HELPER.PY: Before leaving, I suggest scrubbing the data. [Enter]")
                input("HELPER.PY: Head to the bathroom for injection. [Enter]")
                input("HELPER.PY: Leave your pc to make it seem natural. Use your phone's remote access. [Enter]")
                print("* You go the bathroom and boot up systemLink. ")
                input("HELPER.PY: ..\Exfiltration.exe- [Enter]")
                print("""
                    // Initializing NeuraGenix Security Camera System Bypass
                    >>> Accessing camera feed storage...
                    """)
                print("""
                    [Connecting to NeuraGenix security network...]
                    [Bypassing encryption layers...]
                    """)
                print("""
                    [Authorization token spoofed]
                    >>> Camera feed access granted
                    >>> Locating relevant video files...
                    """)
                print("""
                    [Searching for recent surveillance recordings...]
                    >>> Files located: CAM_12_09-2024.log, CAM_13_09-2024.log, CAM_14_09-2024.log
                    """)

                # TASKS HERE
                addScore = mission1Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("""
                >>> Initiating file corruption sequence...
                [Overwriting CAM_12_09-2024.log...]
                >>> 25% complete...
                >>> 50% complete...
                >>> 100% complete - File corrupted
                 """)

                # TASKS HERE
                addScore = mission1Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("[Overwriting CAM_13_09-2024.log...]")
                input(">>> 25% complete...")
                input(">>> 50% complete...")
                input(">>> 100% complete - File corrupted")

                # TASKS HERE
                addScore = mission1Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("[Overwriting CAM_14_09-2024.log...]")
                input(">>> 25% complete...")
                input(">>> 50% complete...")
                input(">>> 100% complete - File corrupted")
                input(">>> Status: All relevant surveillance footage has been erased.")

                # TASKS HERE
                addScore = mission1Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("""
                >>> Initiating log cleanup...
                [Scrubbing access logs...]""")
                input("""
                >>> Log entries for Camera Access successfully deleted
                >>> System audit trail: Clean
                """)
                input(">>> Surveillance bypass complete. No trace detected.")

                # TASKS HERE
                addScore = mission1Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("You've successfully erased incriminating data. ")
                input("Time to head out. Holding a phone in hand and pretending to talk to someone, you leave the premises. ")
                input("You almost forget your laptop, but that will only help sell the trick. ")
                input("Picking up your stuff, you head out of the building. ")

                # Clearing the mission
                print(f"HELPER.PY: Mission completed, score: {missionScore} / {missionScoreMax}. Base Pay: 1000©")
                if missionScore >= missionScoreMax:
                    scoreModifier = 1.15
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore >= 3:
                    scoreModifier = 1
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore < 3:
                    scoreModifier = 0.75
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore >= 0:
                    scoreModifier = 0.5
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                else:
                    scoreModifier = 0.3
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")

                pay(scoreModifier, 1, 2)
                input("HELPER.PY: Mission complete! ")
                missionCompletedScreen()
                print("* Changing location... ")
                travel_menu(maat[1])
                # Update mission status
                cursor = connection.cursor()
                cursor.execute("INSERT INTO mission_accomplished(game_id, mission_id) VALUES (%s, %s)", (player, 1))
                connection.commit()
                cursor.close()
                input("Press enter to continue ")
                clear_console()
                travel_to(airports[2])


                break
            elif moveOption == "3":
                input("You head to the bathroom. ")
                input("Locking yourself in the stall, you begin your work. ")
                input("You install the usb you were provided. This brings out an remote access panel. ")
                input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
                input("USER: K3rn3lGh0$t sent: HEH gotchu now.  (HELPER.PY: [Enter]) ")
                input("USER: K3rn3lGh0$t sent: Jk. We already had your stuff.  (HELPER.PY: [Enter]) ")
                input("USER: K3rn3lGh0$t sent: Anyway, sit back. I'll help ya out. (HELPER.PY: [Enter]) ")
                input("-KGRoot.init .\clientConnection:500.6904-676@LogPoint:6784.1245.3455.000.000:  (HELPER.PY: [Enter]) ")
                input(""" 
                        echo "[INFO] Executing exploit on CVE-2024-1234 - Authentication Bypass Exploit"
                        sleep 2
                        echo "[INFO] Injecting payload..."
                        sleep 3
                        """)
                input("""
                        echo "[SUCCESS] Payload injected successfully. Access granted to internal network. "
                        echo "[INFO] Scanning internal network for accessible resources..."
                        sleep 2
                        """)
                input("""
                        echo "[INFO] Discovered 3 active servers:"
                        sleep 1
                        echo "      [1] FileServer01 - 192.168.1.10"
                        echo "      [2] DatabaseServer - 192.168.1.20"
                        echo "      [3] MailServer - 192.168.1.30"
                        sleep 1
                        """)
                input("""
                        echo "[INFO] Attempting to access DatabaseServer..."
                        sleep 2
                        echo "[SUCCESS] Secure.server access established. -HANDSHAKE- .kg\ForceOpen.exe."
                    """)

                input("""
                    // Initializing NeuraGenix Biometric Security Bypass
                    >>> Initializing facial recognition bypass...
                    [Scanning NeuraGenix executive database...]
                    [Acquiring facial image dataset...]
                    """)
                input("[Generating 3D facial model... 5%]")
                input("[Generating 3D facial model... 34%]")
                input("[Generating 3D facial model... 80%]")
                input("[Generating 3D facial model... 90%]")
                input("""
                    >>> Facial recognition match: 97% accuracy
                    >>> Status: Bypass successful
                    """)
                input("""
                    // Proceeding to voiceprint authentication...
                    >>> Initiating voiceprint data extraction...
                     """)

                # TASKS HERE
                addScore = mission1Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("""
                [Accessing archived audio files...]
                [Extracting voice patterns: Frequency, Pitch, Tone...]
                """)
                input("[Generating synthetic voice model...6%]")
                input("[Generating synthetic voice model...15%]")
                input("[Generating synthetic voice model...68%]")
                input("[Generating synthetic voice model...87%]")
                input("""
                >>> Voiceprint match: 92% accuracy
                >>> Status: Bypass successful
                """)

                # TASKS HERE
                addScore = mission1Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("""
                // Biometric authentication completed
                >>> Access granted to secure files
                >>> Navigating to "Nexus_Prototype" folder...
                """)
                input("""
                [Decrypting folder contents...]
                [Data extraction in progress...]
                """)
                input(">>> 45% complete...")
                input(">>> 80% complete...")
                input(">>> 100% complete!")
                input("""
                >>> Project Nexus data successfully extracted.
                >>> Warning: Security systems triggered. Initiating escape protocol...
                """)

                input("USER: K3rn3lGh0$t sent: Done, got the packet. Rest is on you. (HELPER.PY: [Enter]) ")
                print("______________________________________________________________________________")
                input("Time to head out. Holding a phone in hand and pretending to talk to someone, you leave the premises. ")
                input("By the time you leave the area, you are contacted. ")
                print("______________________________________________________________________________")
                input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
                input("USER: Gh0stP@cket sent: yo ***h*l* you forgot to scrub the data. (HELPER.PY:[Enter]): ")
                input("USER: Gh0stP@cket sent: we got the prototype-data and backdoor access t2u, but this was a miss. (HELPER.PY:[Enter]): ")
                input("USER: Gh0stP@cket sent: we'll mask your entry with a ddos cleanup. (HELPER.PY:[Enter]): ")
                input("USER: Gh0stP@cket sent: next time you better do it proper. (HELPER.PY:[Enter]): ")
                print("______________________________________________________________________________")
                input("HELPER.PY: Your details have been presumably caught by the security cameras. [Enter]")
                input("HELPER.PY: We can hope that the organization manages to wipe the slate. [Enter]")
                input("HELPER.PY: Time to finish here. Awaiting further contact. On standby. [Enter]")

                # Clearing the mission
                print(f"HELPER.PY: Mission completed, score: {missionScore} / {missionScoreMax}. Base Pay: 1000©")
                if missionScore >= missionScoreMax:
                    scoreModifier = 1.15
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore >= 3:
                    scoreModifier = 1
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore < 3:
                    scoreModifier = 0.75
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore >= 0:
                    scoreModifier = 0.5
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                else:
                    scoreModifier = 0.3
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")

                pay(scoreModifier, 1, 2)
                input("HELPER.PY: Continue? ")
                missionCompletedScreen()
                # Update mission status
                cursor = connection.cursor()
                cursor.execute("INSERT INTO mission_accomplished(game_id, mission_id) VALUES (%s, %s)",
                               (player, 1))
                connection.commit()
                cursor.close()

                travel_to(airports[2])

                break
        elif query1_3 == "2":
            print("HELPER.PY: Current available locations are: "
                  "\n>NeuraGenix (inside)<"
                  "\n ")
        elif query1_3 == "3":
            threatLevel = getThreat()
            print(f"HELPER.PY: Analyzing... Threat index is: {threatLevel}")

    #######################################################################################################################

def mission1Tasks(points):
    points = 0
    randValue = random.randint(1, 4)
    while points < 4:
        if randValue == 1:
            task1 = input("Question: What does GMO stand for in biotechnology? ")
            if task1 == "Genetically Modified Organism" or task1 == "genetically modified organism":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randValue == 2:
            task2 = input("Question: Which famous biotechnology tool allows for precise editing of DNA sequences? ")
            if task2 == "CRISPR" or task2 == "crispr":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randValue == 3:
            task3 = input(
                "Question: In which year was the first genetically modified crop, "
                "the Flavr Savr tomato, approved for commercial sale in the U.S.? HELPER.PY: Hint: 90s ")
            if task3 == "1994":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randValue == 4:
            task4 = input(
                "Question: What is the term for the process of transferring genes from one organism to another? ")
            if task4 == "Genetic Engineering" or task4 == "genetic engineering":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
    return points

def mission2():
    #Mission scoretracking
    missionScoreMax = 6
    missionScore = 0
    print(Fore.GREEN)
    print("HELPER.PY: Mission 2")
    # mission location/ country
    airport2 = mission_airport(airports[2])
    country2 = mission_country(maat[2])
    print(f"* You arrived to {airport2} in {country2}")
    print(Fore.GREEN)
    print("* Later on... ")
    #Description-print here

    input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
    # input("USER: Gh0stP@cket sent:  (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: good and ready newbie? (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: our next task is to tackle Cipherium Technologies. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: they deal in encryption to shield dirty corporate secrets. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: apparently they also do black business practices, extortion and monopoly bs (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: this time its all on you but remember that we in this together. (HELPER.PY:[Enter]): ")
    print("______________________________________________________________________________")

    #######################################################################################################################
    # Step 1
    # Locate mission critical data
    step2_1State = 0
    while True:
        if step2_1State == 1:
            breakQuery = input("HELPER.PY: Would you like to enter the Cipherium Tech.? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("Moving to target. ")
                break
            elif breakQuery == "no":
                print("______________________________________________________________________________")
                query2_1 = input("HELPER.PY: What would you like to do?"
                                  "\n(1): Locations "
                                  "\n(2): Web "
                                  "\n(3): Status "
                                  "\n(4): Move "
                                  "\n "
                                  "\nInput: ")
        elif step2_1State == 0:
            print("______________________________________________________________________________")
            query2_1 = input("HELPER.PY: What would you like to do?"
                              "\n(1): Locations "
                              "\n(2): Web "
                              "\n(3): Status "
                              # "\n(4): Move "
                              "\n "
                              "\nInput: ")

        if query2_1 == "1":
            if step2_1State == 0:
                # print("HELPER.PY: ")
                print("HELPER.PY: Current available locations are: "
                      "\n>Home<"
                      "\n ")
            elif step2_1State == 1:
                print("HELPER.PY: Current available locations are: "
                      "\n>Home<"
                      "\n*Cipherium"
                      "\n ")
        elif query2_1 == "2":
            input("HELPER.PY: Searching web for Cipherium home page. [Enter]")
            input("HELPER.PY: Indexing search results. [Enter]")
            input("HELPER.PY: Location data stored. Analyzing route. [Enter]")
            print("HELPER.PY: Cipherium added to locations-list.")
            step2_1State = 1
            print("State updated."
                  "\n ")
        elif query2_1 == "3":
            threatLevel = getThreat()
            print(f"HELPER.PY: Analyzing... Threat index is: {threatLevel}")
        elif query2_1 == "4":
            breakQuery = input("HELPER.PY: Would you like to move to Cipherium Tech.? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("Moving to target. ")
                break
            elif breakQuery == "no":
                print("______________________________________________________________________________")
                query2_1 = input("HELPER.PY: What would you like to do?"
                                  "\n(1): Locations "
                                  "\n(2): Web "
                                  "\n(3): Status "
                                  "\n(4): Move "
                                  "\n "
                                  "\nInput: ")

    #######################################################################################################################
    # Step 2
    # Breach premises, find access to mainframe
    input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
    input("USER: Gh0stP@cket sent: U will need some help with this one. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: we have a mole nearby. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: they have an fake id which you can use to get in. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: once in, you will have to plant the given device in mainframe. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: they will find it eventually, so you have to hide it for long enough. (HELPER.PY:[Enter]): ")
    step2_2State = 0
    while True:
        if step2_2State == 1:
            breakQuery = input("HELPER.PY: Would you like to move to Inner complex? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("Moving in. ")
                break
            elif breakQuery == "no":
                print("______________________________________________________________________________")
                query2_2 = input("HELPER.PY: What would you like to do?"
                                  "\n(1): Check surroundings "
                                  "\n(2): Status "
                                  "\n(3): Move "
                                  "\n "
                                  "\nInput: ")

        elif step2_2State == 0:
            print("______________________________________________________________________________")
            query2_2 = input("HELPER.PY: What would you like to do?"
                              "\n(1): Check surroundings "
                              "\n(2): Status "
                              # "\n(3): Move "
                              "\n "
                              "\nInput: ")

        if query2_2 == "1":
            if step2_2State == 0:
                # input("HELPER.PY: ")
                input("HELPER.PY: You're near the Cipherium main-building. [Enter] ")
                input("HELPER.PY: Your next move should be to find the mole. [Enter] ")
                wantToBroadcast = input("HELPER.PY: Would you like to perform a safe broadcast? [yes/no] ")
                while True:
                    if wantToBroadcast == "yes":
                        input("HELPER.PY: Broadcasting. . . . ")
                        input(". . . .")
                        input(". . .")
                        input(".. .. . ..")
                        print("______________________________________________________________________________")
                        input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
                        input("Anon: Sent: Watch out. ")
                        print("______________________________________________________________________________")
                        print("* Your head is suddenly hit with an annoying pain. ")
                        print("* Falling on your feet is a id-card and a package. Seems to fit the bill. ")
                        print("* You put the id-card on your neck. ")
                        print("______________________________________________________________________________")
                        input("Anon: Sent: <, >, ^, ^, <. Track id: 204 (HELPER.PY:[Enter]) ")
                        print("______________________________________________________________________________")
                        input("HELPER.PY: I would argue that these are directions to the mainframe. "
                              "\nPlease take mental note of these instructions. [Enter] ")
                        step2_2State = 1
                        print("State updated."
                              "\n ")
                        break
                    else:
                        input("HELPER.PY: We need to get in touch with the mole. ")
                        print("______________________________________________________________________________")
                        wantToBroadcast = input("HELPER.PY: Would you like to perform a safe broadcast? [yes/no] ")

            elif step2_2State == 1:
                print("HELPER.PY: Current available locations are: "
                      "\n>Cipherium, outside<"
                      "\n")
        elif query2_2 == "2":
            threatLevel = getThreat()
            print(f"HELPER.PY: Analyzing... Threat index is: {threatLevel}")
        elif query2_2 == "3":
            breakQuery = input("HELPER.PY: Would you like to move to Inner complex? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("Moving in. ")
                break

            elif breakQuery == "no":
                print("______________________________________________________________________________")
                query2_2 = input("HELPER.PY: What would you like to do?"
                                  "\n(1): Check surroundings "
                                  "\n(2): Status "
                                  "\n(3): Move "
                                  "\n "
                                  "\nInput: ")

    #######################################################################################################################
    # Step 3
    # obtain encryption key, plant tracker, cleanup and exit
    step2_3State = 0
    while True:
        if step2_3State == 1:
            print("______________________________________________________________________________")
            breakQuery = input("HELPER.PY: Head home? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("Going home ")
                break
            elif breakQuery == "no":
                print("______________________________________________________________________________")
                query2_3 = input("HELPER.PY: What would you like to do? "
                                   "\n(1): Check surroundings "
                                   "\n(2): Status "
                                   "\n(3): Move "
                                   "\n "
                                   "\nInput: ")
        elif step2_3State == 0:
            print("______________________________________________________________________________")
            query2_3 = input("HELPER.PY: What would you like to do? "
                               "\n(1): Check surroundings "
                               "\n(2): Status "
                               # "\n(3): Move "
                               "\n "
                               "\nInput: ")

        if query2_3 == "1":
            # input("HELPER.PY: ")
            input("* Moving onward to the front door, you're let through no problem with your id on display.")
            input("* In the lobby, you see security scan, helpdesk and IT.")
            print("______________________________________________________________________________")
            roomSurvey = input("HELPER.PY: What would you like to do? "
                               "\n(1): Head to the security scan. "
                               "\n(2): Head to helpdesk. "
                               "\n(3): Head to IT. "
                               "\n "
                               "\nInput: ")

            if roomSurvey == "1":
                print("* You head to the security scan. ")
                input("* You are asked to place your belongings on a security screening. ")
                input("* To prevent suspicion, you comply. "
                      "\nOnly then you do realize that you had a suspicious package with you. ")
                input("* The operator suspends the process so as to check the package. ")
                input("* Gazing upon a strange looking device and asking you what it is, you are dumbfound. ")
                input("* Fight or flight-response kicks in, you try to escape... But you are caught quite easily. ")
                input("* End of the line. Mission status: Critical failure. ")
                loseGame(player)
                break
            elif roomSurvey == "2":
                print("* Heading to helpdesk, you bring about the package you were carrying. ")
                input("* You tell the person in a polite manner, "
                       "\nthat you are busy but that you were asked by your boss to mail "
                       "a prototype encryption-device to a client. ")
                input("* You write a fake address quickly to inform them where it should go. ")
                input("* Slightly confused, but cooperative, "
                       "\nthe person takes the package to the mailroom as you head in with your id. ")
                input("* You take another left from where the assistant was headed but stay in wait after the turn. ")
                input("* You take out your laptop. ")
                print("______________________________________________________________________________")
                input("HELPER.PY: How can I help? [Enter]")
                input("* .\main\-systemLink.enableTracker() ")
                print("Trackers detected. ")
                trackerId = input("HELPER.PY: Please input linked tracker id: ")
                attempts = 0

                #Tracking package
                while True:
                    if trackerId == "204":
                        input("HELPER.PY: Connection established. Tracking.")
                        input("HELPER.PY: Tracking...")
                        input("HELPER.PY: Tracking..")
                        input("HELPER.PY: Path built, result:"
                              "\n ^, ^, <, >")
                        break
                    elif trackerId != "204":
                        attempts += 1
                        print("HELPER.PY: No tracker with given id in range. ")
                        trackerId = input("HELPER.PY: Please input linked tracker id: ")
                    elif attempts > 4:
                        print("HELPER.PY: No more trackers in range. Terminating.")
                        input("* Tracker is out of range, it will be near impossible to recover the package. ")
                        input("* You have no choice but leave the premises. Mission failed.")
                        loseGame(player)
                        break

                print("* You follow the tracked path. (HELPER.PY: Input tracked path: ) ")
                trackPath1 = input("* Tracked path is? (No spaces): ")
                if trackPath1 == "^,^,<,>":
                    input("* You manage to navigate efficiently to the post room. ")
                    missionScore =+1
                elif trackPath1 != "^,^,<,>":
                    input("* You find your way after fumbling about... ")
                    missionScore =-1

                input("* You enter the mailroom in a hurry and ask about a prototype-package. ")
                input("* You tell the mailroom person, that there was a critical bug in the package which needs to be resolved. ")
                input("* Confused but cooperating, the staffmember gives the package. ")
                input("* You thank the worker with relief, stating that it could have been critically dangerous to send it as is. ")
                input("* The worker seemed relieved and happy. ")

                input("* Holding the package once more. It is now time to find a way to the mainframe. ")
                print("______________________________________________________________________________")
                mainFrameDirections = input("HELPER.PY: Do you still remember the provided directions?"
                                            "\n(Direction, no spaces): ")

                if mainFrameDirections == "<,>,^,^,<":
                    print("* You make your way through the large building complex. You skillfully avert eyes and seem natural in your movement. ")
                    missionScore =+1
                elif mainFrameDirections != "<,>,^,^,<":
                    print("* You take a long time to find your way in the complex. By the time you arrive, 1,5 hours have passed. ")
                    #Increase threat
                    raiseThreat("failure")
                    missionScore =-1

                print("* You head inside the mainframe. ")
                input("* You navigate the room to find a remote corner as hidden from public view as possible. ")
                input("* Installing the device, you begin the process of file decryption. ")
                print("______________________________________________________________________________")
                input("HELPER.PY: Injecting data parser algorithm. ")

                #TASK HERE
                addScore = mission2Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input(
                """
                import _package
                protected: handshake(message, duration):
                    print(message, end="", flush=True)
                    for _ in range(duration):
                        time.sleep(0.5)
                        print(".", end="", flush=True)
                """)

                #TASK HERE
                addScore = mission2Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("""
                print()
                protected: data_collection():
                    print("Initiating data extraction.")
                    display_loading_message("Datalink", 5)
                    display_loading_message("Download", 7)
                    print("Analysis:")
                """)

                #TASK HERE
                addScore = mission2Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("""
                for i in range(5):
                        data_size = random.randint(100, 500)
                        time.sleep(1)
                        print(f  Package analysis: {i+1}/5: {data_size} Mt)
                    display_loading_message(Verify, 5)
                    print(Extraction)
                    print(Parse)
                    print(Sending data)
                data_collection()
                """)

                input("HELPER.PY: Datalink established. ")
                input("* Mission parameters completed. Time to leave. ")
                print("* You leave the premises, leaving the tracker behind."
                      "\nIt should be able to gather incriminating evidence in due time.")

                # Clearing the mission
                print(f"HELPER.PY: Mission completed, score: {missionScore} / {missionScoreMax}. Base Pay: 1000©")
                if missionScore >= missionScoreMax:
                    scoreModifier = 1.15
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore >= 3:
                    scoreModifier = 1
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore < 3:
                    scoreModifier = 0.75
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore >= 0:
                    scoreModifier = 0.5
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                else:
                    scoreModifier = 0.3
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")

                pay2(scoreModifier, 2)
                input("HELPER.PY: Mission complete! ")
                missionCompletedScreen()
                # Update mission status
                cursor = connection.cursor()
                cursor.execute("INSERT INTO mission_accomplished(game_id, mission_id) VALUES (%s, %s)",
                               (player, 2))
                connection.commit()
                cursor.close()

                break
            elif roomSurvey == "3":
                input("* You head on to IT. ")
                input("* You hand out the package in your hand, claiming it's broken and needs looking into. ")
                input("* The person opens the package and sees a strange looking device. ")
                input("* The person asks you what it is. ")
                input("* Without having thought about what it might be, "
                      "\nyou fumble in your words and end up calling it a prototype encryption device. ")
                input("* The person doesn't seem to care too much and passes the device along. ")
                input("* They tell you that they will look into it asap but for now they will need your contact details. ")
                input("* You give them a fake contact form and thank them as you head out. ")

                input("* You take out your laptop. ")
                print("______________________________________________________________________________")
                input("HELPER.PY: How can I help? [Enter]")
                input("* .\main\-systemLink.enableTracker() ")
                print("Trackers detected. ")

                # Tracking package
                trackerId = input("HELPER.PY: Please input linked tracker id: ")
                attempts = 0

                # Tracking package
                while True:
                    print("HELPER.PY: No tracker with given id in range. ")
                    if trackerId == "204":
                        input("HELPER.PY: Connection established. Tracking.")
                        input("HELPER.PY: Tracking...")
                        input("HELPER.PY:Tracking..")
                        input("HELPER.PY: Path built, result:"
                              "\n ^, ^, <, >")
                        break
                    elif trackerId != "204":
                        attempts += 1
                        print("HELPER.PY: No suck tracker in range. ")
                        trackerId = input("HELPER.PY: Please input linked tracker id: ")
                    elif attempts > 4:
                        print("HELPER.PY: No more trackers in range. Terminating.")
                        input("* Tracker is out of range, it will be near impossible to recover the package. ")
                        input("* You have no choice but leave the premises. Mission failed.")
                        loseGame(player)
                        break

                input("* You realize that the tracker isn't moving. ")
                input("* You're going to have to wait to be able to recover the device. ")
                input("* You wait in a nearby bathroom for a long time before the tracker provides you with new movement. ")
                input("* The tracker eventually moves to a location where you are able to fetch it from another person. ")
                missionScore =- 2

                input("* Holding the package once more. It is now time to find a way to the mainframe. ")
                print("______________________________________________________________________________")
                mainFrameDirections = input("HELPER.PY: Do you still remember the provided directions?"
                                            "\n(Direction, no spaces): ")

                if mainFrameDirections == "<,>,^,^,<":
                    print(
                        "* You make your way through the large building complex. You skillfully avert eyes and seem natural in your movement. ")
                    missionScore = +1
                elif mainFrameDirections != "<,>,^,^,<":
                    print(
                        "* You take a long time to find your way in the complex. By the time you arrive, 1,5 hours have passed. ")
                    # Increase threat
                    missionScore = -1

                print("* You head inside the mainframe. ")
                input("* You navigate the room to find a remote corner as hidden from public view as possible. ")
                input("* Installing the device, you begin the process of file decryption. ")
                print("______________________________________________________________________________")
                input("HELPER.PY: Injecting data parser algorithm. ")

                # TASK HERE
                addScore = mission2Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input(
                    """
                    import _package
                    protected: handshake(message, duration):
                        print(message, end="", flush=True)
                        for _ in range(duration):
                            time.sleep(0.5)
                            print(".", end="", flush=True)
                    """)

                # TASK HERE
                addScore = mission2Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("""
                    print()
                    protected: data_collection():
                        print("Initiating data extraction.")
                        display_loading_message("Datalink", 5)
                        display_loading_message("Download", 7)
                        print("Analysis:")
                    """)

                # TASK HERE
                addScore = mission2Tasks(missionScore)
                missionScore += addScore
                print(f"HELPER.PY: Mission Progress: {missionScore} / {missionScoreMax}. ")
                threatLevel = getThreat()
                print(f"HELPER.PY: Threat index is: {threatLevel}. ")
                # WARNING
                if threatLevel >= 40:
                    input("HELPER.PY: /!\WARNING/!\: Threat-level increased."
                          "\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")

                input("""
                    for i in range(5):
                            data_size = random.randint(100, 500)
                            time.sleep(1)
                            print(f  Package analysis: {i+1}/5: {data_size} Mt)
                        display_loading_message(Verify, 5)
                        print(Extraction)
                        print(Parse)
                        print(Sending data)
                    data_collection()
                    """)

                input("HELPER.PY: Datalink established. ")
                input("* Mission parameters completed. Time to leave. ")
                print("* You leave the premises, leaving the tracker behind."
                      "\nIt should be able to gather incriminating evidence in due time.")

                # Clearing the mission
                print(f"HELPER.PY: Mission completed, score: {missionScore} / {missionScoreMax}. Base Pay: 1000©")
                if missionScore >= missionScoreMax:
                    scoreModifier = 1.15
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore >= 3:
                    scoreModifier = 1
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore < 3:
                    scoreModifier = 0.75
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                elif missionScore >= 0:
                    scoreModifier = 0.5
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")
                else:
                    scoreModifier = 0.3
                    input(f"Score modifier: {missionScore}/{missionScoreMax} = {scoreModifier}."
                          f"\nPay: {1000 * scoreModifier}.")

                pay2(scoreModifier, 2)
                input("HELPER.PY: Mission complete! ")
                missionCompletedScreen()
                # Update mission status
                cursor = connection.cursor()
                cursor.execute("INSERT INTO mission_accomplished(game_id, mission_id) VALUES (%s, %s)",
                               (player, 2))
                connection.commit()
                cursor.close()

                break
        elif query2_3 == "2":
            threatLevel = getThreat()
            print(f"HELPER.PY: Analyzing... Threat index is: {threatLevel}")
        elif query2_3 == "3":
            if step2_3State == 1:
                breakQuery = input("HELPER.PY: Head home? (HELPER.PY:[yes/no]): ")
                if breakQuery == "yes":
                    print("Going home. ")
                    break
                elif breakQuery == "no":
                    print("______________________________________________________________________________")
                    query2_3 = input("HELPER.PY: What would you like to do?"
                                      "\n(1): Check surroundings "
                                      "\n(2): Status "
                                      "\n(3): Move "
                                      "\n "
                                      "\nInput: ")
            elif step2_3State == 0:
                print("______________________________________________________________________________")
                stateQuery = input("HELPER.PY: What would you like to do? "
                                   "\n(1): Check surroundings "
                                   "\n(2): Status "
                                   # "\n(3): Move "
                                   "\n "
                                   "\nInput: ")

def mission2Tasks(points):
    points = 0
    randomValue = random.randint(1, 10)
    while True:
        if randomValue == 1:
            task1 = input("Solve the following sentence using Caesar Shift -1: 'fnnc ktbj rzuhmf sgd vnqkc'\n")
            if task1 == "good luck saving the world":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randomValue == 2:
            task2 = input("Solve the following word using Caesar Shift -1: 'gnknfqzl'\n")
            if task2 == "hologram":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
        elif randomValue == 3:
            task3 = input("Solve the following sentence using Caesar Shift -1: 'zqd xnt rdqhntr'\n")
            if task3 == "are you serious":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randomValue == 4:
            task4 = input("Solve the following sentence using Caesar Shift -1: 'fnnc lnqmhmf uhdszml'\n")
            if task4 == "good morning vietnam":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randomValue == 5:
            task5 = input("Solve the following sentence using Caesar Shift +1: 'xfmm epof jt cfuufs uibo xfmm tbje'\n")
            if task5 == "well done is better than well said":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randomValue == 6:
            task6 = input("Solve the following words using Caesar Shift +1: 'qsjwbsb dbqjubm'\n")
            if task6 == "privara capital":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randomValue == 7:
            task7 = input("Solve the following word using Caesar Shift +1: 'ofvsbhfojy'\n")
            if task7 == "neuragenix":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randomValue == 8:
            task8 = input("Solve the following words using Caesar Shift +1: 'ofuxpsl qspupdpm'\n")
            if task8 == "network protocol":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randomValue == 9:
            task9 = input("Solve the following word using Caesar Shift +1: 'bvuifoujdbujpo'\n")
            if task9 == "authentication":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
        elif randomValue == 10:
            task10 = input("Solve the following word using Caesar Shift +1: 'lfsofm qbojd'\n")
            if task10 == "kernel panic":
                print("access_point_status: GREEN")
                points += 1
                return points
            else:
                print("ERROR: Faulty user input...")
                raiseThreat("failure")
    return points


# FUNKTIOT PÄÄTTYY
########################################################################################################################
# MAIN

print(Fore.GREEN)
print(Style.BRIGHT)

# Soitetaan taustamusiikki loopattuna asynkronisesti (ei pysäytä ohjelmaa)
playback = Playback()  # creates an object for managing playback of a single audio file
playback.load_file('bgmusicexample.mp3')
playback.loop_at_end(True)
playback.play()

maat = []
airports = []

player = init()

currentMission = False

#websivut = {
#    "ghostrepo.net": """
#    ghostrepo.net
#
#   Testi
#    Testi
#    Testi
#    """,
#    "privaracapital.org": """
#    privaracapital.org
#
#    Testi
#    testi
#    testi
#    """
#}

# Alustetaan alkuruutu-animaation sisältö monirivisellä tekstillä

alkuanimaatioruutu = """
░▒▓█▓▒   ▒▓██████████████▓▒░      ░▒▓█▓▒   ▒▓███████▓▒░  
░▒▓█▓▒   ▒▓█▓▒  ▒▓█▓▒  ▒▓█▓▒░     ░▒▓█▓▒   ▒▓█▓▒  ▒▓█▓▒░ 
░▒▓█▓▒   ▒▓█▓▒  ▒▓█▓▒  ▒▓█▓▒░     ░▒▓█▓▒   ▒▓█▓▒  ▒▓█▓▒░ 
░▒▓█▓▒   ▒▓█▓▒  ▒▓█▓▒  ▒▓█▓▒░     ░▒▓█▓▒   ▒▓█▓▒  ▒▓█▓▒░ 
░▒▓█▓▒   ▒▓█▓▒  ▒▓█▓▒  ▒▓█▓▒░     ░▒▓█▓▒   ▒▓█▓▒  ▒▓█▓▒░ 
                                    Hacker on board...

"""

# Häviö animaatio
havioanimaatioruutu = """                                       
    @@@     @@@@@@@@@@@@@@@@@@@@@@@@@@     @@@    
  @@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@  
    @@@@  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@   
      @@@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@     
        @ @@@        @@@@@@@        @@@ @       
          @@    o    @@@@@@@    o    @@         
          @@@       @@@@ @@@@       @@@         
          @@@@@@@@@@@@@   @@@@@@@@@@@@@         
           @@@@@@@@@@@@@@@@@@@@@@@@@@@         
         @   @@ @L @O @S @E @R @! @@   @        
       @@@@  @@ L@ O@ S@ E@ R@ !@ @@  @@@@ 
   @@@@@@     @@@@@@@@@@@@@@@@@@@@@    @@@@@@@  
     @@@@      @@@@@@@@@@@@@@@@@@@     @@@@      
"""

voittoanimaatioruutu = """
              @              
             @@@             
              @              
       @      @      @       
 @     @@    @@@    @@     @ 
  @@   @@@  @@@@@  @@@   @@  
   @@  @@@@ @@@@@ @@@@  @@@  
   @@@@@@@@@@@@@@@@@@@@@@@   
    @@@@@@@@@@@@@@@@@@@@@    
     @@@@@@@@@@@@@@@@@@@     
      @@@@@@@@@@@@@@@@@     
      @@             @@      
"""

# Alustetaan loppuruutu-animaation sisältö monirivisellä tekstillä
loppuanimaatioruutu = """
Epic Cinematic Gaming Cyberpunk | RESET by Alex-Productions | https://onsound.eu/
Music promoted by https://www.chosic.com/free-music/all/
Creative Commons CC BY 3.0
https://creativecommons.org/licenses/by/3.0/

..::CREDITS::..
Tim Fabritius                Svetlana Kekkonen-Mattila    Mikko Laakkonen                   Joni Oksanen             Outi Salonen
-Graphics programming        -Database design             -Narrative design                 -Gameplay design         -Design QA
-System design               -Funcition programming       -Gameplay programming & design    -Mechanics programming   -Documentation
-Database design             -Travel design               -Graphic design                   -UI programming
-Function programming        -Gameplay QA                 -Documentation                    -Gameplay QA
"""

# TIMIN FUNKTIOT
# startScreen()
# loseScreen()
# endScreen()
# winScreen()
# openWeb("ghostrepo.net")
# tmp = calcPrice("EFHK","ESSA")
# print(tmp)
# tmp = calcCO2("EFHK","ESSA")
# print(tmp)
# pay(1,0,1)
# raiseThreat('failure')
# lowerThreat()

# MIKON FUNKTIOT
# mission0()
# mission1()
# mission1Tasks()
# mission2()
# mission2Tasks()

# JONIN FUNKTIOT
# init()
# loseGame(player)
# winGame(player)
# optionMenu()
# pauseMenu()

# Svetlanan funktiot
#travel_menu("FI")
# travel_to("EFHK")
#mission_airport(airports[1])
#mission_country(maat[1])


#INTRO
startScreen()

# PÄÄOHJELMA

completed_missions_count = check_completed_missions()
if completed_missions_count == 0:
    mission0()
    completed_missions_count = check_completed_missions()

if completed_missions_count == 1:
    mission1()
    completed_missions_count = check_completed_missions()

if completed_missions_count == 2:
    mission2()
    completed_missions_count = check_completed_missions()

if completed_missions_count == 3:
    endScreen()
    winGame(player)
    #winScreen()