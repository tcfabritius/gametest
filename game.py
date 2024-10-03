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
    cursor = connection.cursor()
    cursor.execute("select latitude_deg, longitude_deg from airport where ident = %s", (icao1,))
    sijainti1 = cursor.fetchall()
    cursor = connection.cursor()
    cursor.execute("select latitude_deg, longitude_deg from airport where ident = %s", (icao2,))
    sijainti2 = cursor.fetchall()
    hinta = int(distance.distance(sijainti1, sijainti2).km) * 1
    cursor.close()
    return hinta


def raiseThreat(type):
    cursor = connection.cursor()
    cursor.execute("SELECT threat FROM game WHERE id = %s", (player,))
    threat = cursor.fetchone()
    threat = int(threat[0])
    if type == "stay":
        if threat + 1 > 100:
            loseGame()
        else:
            cursor.execute("UPDATE game SET threat = threat +1 WHERE id = %s", (player,))
            connection.commit()

    if type == "failure":
        if threat + 3 > 100:
            loseGame()
        else:
            cursor.execute("UPDATE game SET threat = threat +3 WHERE id = %s", (player,))
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


def openWeb(webpage):
    clear_console()
    print("")
    print(Fore.GREEN + websivut[webpage])
    tmp = input("Press enter to exit web browser")
    print(Style.RESET_ALL)
    clear_console()


def travel_to(icao_target):
    cursor = connection.cursor()
    cursor.execute("SELECT game.location FROM game, airport WHERE game.id = %s", (player,))
    location_c = cursor.fetchone()
    current_location = location_c[0]
    target = icao_target
    travel_price = calcPrice(current_location, target)

    cursor = connection.cursor()
    cursor.execute("select money from game WHERE id = %s", (player,))
    saldo = cursor.fetchall()
    atm_saldo = int(saldo[0][0])
    if travel_price > atm_saldo:
        loseGame(player)

    travel_co2 = calcCO2(current_location, target)
    # update location

    cursor = connection.cursor()
    sql_target = f"UPDATE game SET location = (SELECT ident FROM airport WHERE ident = '{target}'),co2_consumed = co2_consumed+'{travel_co2}' WHERE id ='{player}'"
    cursor.execute(sql_target)
    connection.commit()

    cursor = connection.cursor()
    cursor.execute("SELECT game.co2_budget FROM game WHERE game.id = %s", (player,))
    budget_co2 = cursor.fetchone()
    co2_budget = budget_co2[0]
    # print(co2_budget)
    # if travel_co2 > co2_budget: ??? co2_budgetti on liian pieni
    # loseGame()

    # update money
    cursor = connection.cursor()
    sql_money = f"UPDATE game SET money = (money -'{travel_price}') WHERE id ='{player}'"
    cursor.execute(sql_money)
    connection.commit()
    cursor = connection.cursor()
    cursor.execute("SELECT game.money FROM game WHERE game.id = %s", (player,))
    money_left = cursor.fetchone()
    print(f"Money left in the budget: {money_left[0]}€")
    # lowerThreat()
    cursor.close()


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

    # print menu
    print("\nAvailable Airports: \n")

    for (a, b, c, d) in zip(icao, names, prices, co2):
        print(f"{a}  {b} \n      price: {c}  CO2(ppm): {d}\n")

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
    loseScreen()
    # Suljetaan kursori ja yhteys
    cursor.close()

    goBack = input("Press Enter to go back to Main Menu: ")
    if goBack == "":
        pauseMenu()
    return


def winGame(player):
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
    winScreen()
    # Suljetaan kursori ja yhteys
    cursor.close()

    print(
        "THANK YOU FOR PLAYING THE GAME!\nCREDITS:\nTim Fabritius\nSvetlana Kekkonen-Mattila\nMikko Laakkonen\nJoni Oksanen\nOuti Salonen")

    goBack = input("Press Enter to go back to Main Menu: ")
    if goBack == "":
        pauseMenu()
    return


def optionMenu():
    # VALINTAMENU
    print("Choose action to proceed:\n1.Hack\n2.Web\n3.Buy\n4.Back to Main Menu ")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        if currentMission == True:
            winScreen()
        elif currentMission == False:
            loseGame()
    elif choice == 2:
        openWeb()
    elif choice == 3:
        openShop()
    elif choice == 4:
        pauseMenu()


def openShop():
    print("Kauppa")


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
    print("Pause Menu\n1.Start Game\n2.Delete Player\n3.Quit Game\n ")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        init()
    elif choice == 2:
        reset(player)
    elif choice == 3:
        quitGame()

    # PELAAJAN NIMEN KYSYMINEN JA ALKUTIETOJEN ASETTELU. AIKAISEMMAN PELAAJAN TUNNISTAMINEN


def init():
    # Kysytään pelaajan nimi
    print("HACKING USER ID DATABASE...\nACCESS GRANTED...")
    player = input("USE ALIAS: ")

    # Luodaan kursori
    cursor = connection.cursor()
    # Maiden arpominen
    countries_sql = f"SELECT iso_country FROM country ORDER BY RAND() LIMIT 3"
    result = cursor.execute(countries_sql)
    countries = cursor.fetchall()
    for country in countries:
        global maat
        maat.append(country[0])

    for maa in maat:
        airports_sql = f"SELECT ident FROM airport WHERE iso_country = '{maa}' ORDER BY RAND() LIMIT 1"
        result = cursor.execute(airports_sql)
        airport = cursor.fetchall()
        global airports
        airports.append(airport[0][0])


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
    # Mission 0 - Tutorial
    # After playerGreeting
    input(f"USER: Gh0stP@cket sent: cool moves '{player}' lmao. (HELPER.PY:[Enter]: (Input whatever to progress)): ")

    joinInput = input(f"User: Gh0stP@cket sent: wanna join? (HELPER.PY: Type yes if you want to join.): ")

    if joinInput == "yes":
        input("USER: Gh0stP@cket sent: sweet, go to ghostrepo.net and check details. (HELPER.PY:[Enter]): ")
    else:
        input("USER: Gh0stP@cket sent: unlucky lol bye (HELPER.PY:[Enter]): ")
        # Ghostpacker infilitrates your pc here.
        print("""
              $ sudo ls /var/log
              access.log  syslog.log  .hidden
              $ sudo cat /var/log/.hidden
              Error: Permission Denied
              $ sudo chmod 777 /var/log/.hidden
              $ sudo cat /var/log/.hidden
              [ROOTKIT] Installing stealth modules...
              [ROOTKIT] Patching kernel hooks...
              [ROOTKIT] Redirecting network traffic to 192.168.1.100...
              [ROOTKIT] Disabling system logging...
              [ROOTKIT] Erasing traces from /var/log/...
              [ROOTKIT] Operation complete. System compromised.
              $ sudo ls /dev/
              tty1  tty2  null  zero  backdoor  sd0
              $ ps aux | grep -i backdoor
              root      1337  0.0  0.0  0.0    /usr/lib/backdoor.sh
              $ sudo kill -9 1337
              Error: Process cannot be terminated
              byeAndEat****
              $ echo 'System integrity compromised.'
              """)

        # Probably needs a loop that doesn't swap to function call right away after receiving a message.
        # Player should/could lose the game here for giving a wrong answer maybe(?) For the keks.
        # loseTheGame()

    # Player checks given website through the web-tab
    # enterWebUrl("requiredUrl")
    print("YOU: ghostrepo.net")

    input("USER: Gh0stP@cket sent: lol ty (HELPER.PY:[Enter]): ")

    print("""
          $ sudo chmod 777 /var/log/.hidden
          $ sudo cat /var/log/.hidden
          [ROOTKIT] Installing stealth modules...
          [ROOTKIT] Patching kernel hooks...
          [ROOTKIT] Redirecting network traffic to 192.168.1.100...
          [ROOTKIT] Disabling system logging...
          [ROOTKIT] Erasing traces from /var/log/...
          [ROOTKIT] Operation complete. System compromised.
          $ sudo ls /dev/
          tty1  tty2  null  zero  backdoor  sd0
          $ ps aux | grep -i backdoor
          root      1337  0.0  0.0  0.0    /usr/lib/backdoor.sh
          $ sudo kill -9 1337
          Error: Process cannot be terminated
          """)

    input("User: Gh0stP@cket sent: pretty incredible you walked right in that. (HELPER.PY:[Enter]): ")

    input("User: Gh0stP@cket sent: Figured you might be bit brighter. (HELPER.PY:[Enter]): ")

    input("User: Gh0stP@cket sent: w/e.\nif you want your encrypted files back without being spread to whoever, "
          "we need to have some insurance. (HELPER.PY:[Enter]): ")

    input("User: Gh0stP@cket sent: you got in through the backdoor we set up for eager beavers scuch as you."
          "\nfind a way in to privara capital."
          "\nyou should know where to transfer. (HELPER.PY:[Enter]): ")

    print(
        """YOU:
        * set_current_groups - Change current's group subscription
        * @group_info: The group list to impose
        * Validate a group subscription and, if valid, impose it upon current's task
        * security record.
        int set_current_groups(struct group_info *group_info)
        {
        struct cred *new;
          int ret;
          new = prepare_creds();
          if (!new)
              return -ENOMEM;
          ret = set_groups(new, group_info);
            if (ret < 0) {
              abort_creds(new);
              return ret;
          }
          return commit_creds(new);
        }
        """)

    input(
        "HELPER.PY: You probably want to follow the lead on the web. Check: privaraCapital.org on the web. (HELPER.PY:[Enter]): ")

    # Player goes to website - learns more about going to web for info.
    print("YOU: privaraCapital.org")
    # We might need an active message display somewhere after all(?)
    input(
        "HELPER.PY: Username ghostpacket wanted you to infiltrate their crm and internal cashflow via an atm.(HELPER.PY:[Enter]): ")

    print("YOU: Option 3 - Become a client at Privara")

    # Fake bank fake account
    newPrivaraKey = random.randint(1000, 9999)  # Luo satunnaisen 4-numeroisen avaintunnuksen
    print(f"Your 4-digit key is: {newPrivaraKey}")
    newPrivaraPassword = int(input("Please input new password: "))

    print("Password set.")
    input("HELPER.PY: Please take mental note of these credentials. (HELPER.PY:[Enter]): ")

    privaraKey = int(input(f"Please input your 4-letter id: "))
    privaraPassword = int(input(f"Please input your password: "))
    while True:
        if privaraPassword == newPrivaraPassword and privaraKey == newPrivaraKey:
            print("Log in successful.")
            break
        else:
            print("Log in failed.")
            input("HELPER.PY: Please try again. (HELPER.PY:[Enter]): ")
            privaraKey = input(f"Please input your 4-letter id: ")
            privaraPassword = input(f"Please input your password: ")

    print("YOU: USE: rootkit")
    print("""
    $ sudo dmesg | tail
    [13562.33] USB device 3-1: New USB device connected, idVendor=16d0, idProduct=0af2
    [13562.35] USB device 3-1: HID device initialized
    [13562.37] Rootkit module loaded from /dev/usb/backdoor
    [13562.40] Kernel hook injected at 0xFFFF0A34...
    [13562.42] Rootkit process initiated...

    $ ls /dev/usb/
    backdoor    rootkit.sh    terminal.txt

    $ sudo cat /dev/usb/rootkit.sh
    #!/bin/bash
    echo "[ROOTKIT] Accessing bank transaction logs..."
    sleep 1
    echo "[ROOTKIT] Re-routing transactions to 192.168.1.200..."
    sleep 1
    echo "[ROOTKIT] Masking malicious activity in logs..."
    sleep 1
    echo "[ROOTKIT] Uploading data to external server..."

    $ sudo netstat -an | grep 192.168.1.200
    tcp        0      0 192.168.1.50:45328     192.168.1.200:8080     ESTABLISHED

    $ sudo ps aux | grep rootkit
    root       3137  0.0  0.1  13672  2640 ?        S    10:32   0:00 /dev/usb/rootkit.sh
    root       3151  0.0  0.0   6428  1144 ?        S    10:32   0:00 /usr/lib/backdoor

    $ echo "System compromise in progress."
    """)

    # Player will do one mission task here.
    while True:
        firstTask = input("access_point 20: int2**3*int5\nCaseFalse =? ")
        if firstTask == "yes" or "true":
            print("ERROR: Critical user error.")
        elif firstTask == "no" or "false":
            correctAnswer = int(input("Please input correct variable: "))
            if correctAnswer == 40:
                print("access_point 20: STATUS: GREEN")
                break

    # Teach about the threat-mechanic via intrusion
    print(
        "HELPER.PY: /!\WARNING/!\: Threat-level increased.\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")
    # Here is where we update the threat level for the first time.

    # Player goes home
    print("HELPER.PY: Going home...")

    input("USER: Gh0stP@cket sent: bit sloppy but you did the trick (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: package in money out, nice work (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: ill vouch for you, welcome aboard newbie. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: if youre wandering about the bank you just broke into... (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: bunch of cashgrabbers and ******* scam-artists. (HELPER.PY:[Enter]): ")
    input(
        "USER: Gh0stP@cket sent: t2u theyre going to be sorting through their **** for a while. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: that and K3rn3lGh0$t injectors. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: anyway, now thats done. Time to move on to bigger fish. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: this world is full of rot and we were needing some new blood. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: get out there. (HELPER.PY:[Enter]): ")
    print(f"(HELPER.PY:[Enter]): Guided mission protocol over. Good luck {player}")
    print(Style.RESET_ALL)


def mission1():
    # Biotech aiheinen tehtävä
    print("Mission 1")
    input("NeuraGenix is renowned for its implant technology. "
          "\nBreach NeuraGenix's systems and steal the classified ”Nexus”-project. "
          "\nThe company is very cagey, so verify for potentially malicious intent. "
          "\n(HELPER.PY:[Enter]): ")

    input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
    # input("USER: Gh0stP@cket sent:  (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: all set newbie? (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: theres this big pile of a company called NeuraGenix. (HELPER.PY:[Enter]): ")
    input(
        "USER: Gh0stP@cket sent: not that theyre entirely rotten, they just kinda exist on a bad frontier. (HELPER.PY:[Enter]): ")
    input(
        "USER: Gh0stP@cket sent: owner of xitter is already pushing buttons with their neuralink bs but nothing as major as these guys. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: unlucky however fact however is that theyre being quiet."
          "\nBig sus that they might be in cahoots with someone they shouldnt. (HELPER.PY:[Enter]): ")
    input(
        "USER: Gh0stP@cket sent: anyway. Sent ya smth. Should help with biometrics but otherwise its in your hands. (HELPER.PY:[Enter]): ")
    input(
        "USER: Gh0stP@cket sent: youre in but youre still on the lookout before we vest in you fully. (HELPER.PY:[Enter]): ")

    #######################################################################################################################
    # Step 1
    step1State = 0
    while True:
        if step1State == 1:
            breakQuery = input("HELPER.PY: Would you like to move to NeuraGenix? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("HELPER.PY: Moving to target. ")
                break
            elif breakQuery == "no":
                branch2_1 = input("HELPER.PY: What would you like to do?"
                                  "\n(1): Check delivery "
                                  "\n(2): Locations "
                                  "\n(3): Web "
                                  "\n(4): Status "
                                  "\n(5): Move "
                                  "\n "
                                  "\nInput: ")
        elif step1State == 0:
            branch2_1 = input("HELPER.PY: What would you like to do?"
                              "\n(1): Check delivery "
                              "\n(2): Locations "
                              "\n(3): Web "
                              "\n(4): Status "
                              # "\n(5): Move "
                              "\n "
                              "\nInput: ")

            if branch2_1 == "1":
                print(
                    "HELPER.PY: You were sent a usb-drive. It seems to contain a bypass-program. Note inside says: 'Get me in their intra. -KeGh'")
            elif branch2_1 == "2":
                if step1State == 0:
                    # print("HELPER.PY: ")
                    print("HELPER.PY: Current available locations are: "
                          "\n>Home<"
                          "\n ")
                elif step1State == 1:
                    print("HELPER.PY: Current available locations are: "
                          "\n>Home<"
                          "\n*NeuraGenix"
                          "\n ")
            elif branch2_1 == "3":
                input("HELPER.PY: Searching web for NeuraGenix home page. [Enter]")
                input("HELPER.PY: Indexing search results. [Enter]")
                input("HELPER.PY: Location data stored. Analyzing route. [Enter]")
                print("HELPER.PY: NeuraGenix added to locations-list.")
                step1State = 1
                print("State updated."
                      "\n ")
            elif branch2_1 == "4":
                print(f"Your current threat level is: blahblah"
                      f"\n ")
            elif branch2_1 == "5":
                breakQuery = input("HELPER.PY: Would you like to move to NeuraGenix? (HELPER.PY:[yes/no]): ")
                if breakQuery == "yes":
                    print("HELPER.PY: Moving to target.")
                    break
                elif breakQuery == "no":
                    branch2_1 = input("HELPER.PY: What would you like to do?"
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
        step2State = 0
        while True:
            if step2State == 1:
                breakQuery = input("HELPER.PY: Head inside NeuraGenix? (HELPER.PY:[yes/no]): ")
                if breakQuery == "yes":
                    print("HELPER.PY: Entering building. ")
                    break
                elif breakQuery == "no":
                    branch2_2 = input("HELPER.PY: What would you like to do? "
                                      "\n(1): Check surroundings"
                                      "\n(2): Locations "
                                      "\n(3): Status "
                                      "\n(4): Move "
                                      "\n "
                                      "\nInput: ")
            elif step2State == 0:
                branch2_2 = input("HELPER.PY: What would you like to do? "
                                  "\n(1): Check surroundings"
                                  "\n(2): Locations "
                                  "\n(3): Status "
                                  # "\n(4): Move "
                                  "\n "
                                  "\nInput: ")

            if branch2_2 == "1":
                input(
                    "HELPER.PY: You are currently outside NeuraGenix. There are guards posted at the front entrance. [Enter]")
                input("HELPER.PY: You will not be able to get in with your current status. [Enter]")
                input(
                    "HELPER.PY: There's a cafeteria within the block vicinity. We should head on over and perform a local network-scan. [Enter]")
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
                        input("HELPER.PY: Package analysis 5/125... ")
                        input("HELPER.PY: Package analysis 23/125... ")
                        input("HELPER.PY: Package analysis 50/125... ")
                        input("HELPER.PY: Package analysis 78/125... ")
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

                            input("""
                            echo "[INFO] Executing exploit on CVE-2024-1234 - Authentication Bypass Exploit"
                            sleep 2
                            echo "[INFO] Injecting payload..."
                            sleep 3
                            echo "[SUCCESS] Payload injected successfully. Access granted to internal network. "
                            """)

                            # TASKS HERE

                            input("""
                            echo "[INFO] Scanning internal network for accessible resources..."
                            sleep 2
                            echo "[INFO] Discovered 3 active servers:"
                            sleep 1
                            echo "      [1] FileServer01 - 192.168.1.10"
                            echo "      [2] DatabaseServer - 192.168.1.20"
                            echo "      [3] MailServer - 192.168.1.30"
                            sleep 1
                            echo "[INFO] Attempting to access DatabaseServer..."
                            sleep 2
                            echo "[INFO] Failure, biometric security detected."
                            sleep 1
                            echo "[INFO] Generating id data."
                            sleep 1
                            echo "[SUCCESS] ID data generated."
                            sleep 1
                            echo "[SUCCESS] Access id linked with RFID."
                            sleep 1
                            echo "[INFO] Command finished. Quitting program... Cleaning logs... "
                            """)
                            step2State = 1
                            print("State updated. "
                                  "\n")
                            break
                        else:
                            input("HELPER.PY: Entry-probe disabled. Cleaning logs. ")

            elif branch2_2 == "2":
                if step2State == 0:
                    print("HELPER.PY: Current available locations are: "
                          "\n>NeuraGenix<"
                          "\n ")
                elif step2State == 1:
                    print("HELPER.PY: Current available locations are: "
                          "\n*NeuraGenix"
                          "\n>Cafeteria<"
                          "\n ")
            elif branch2_2 == "3":
                print(f"Your current threat level is: blahblah"
                      f"\n ")
            elif branch2_2 == "4":
                breakQuery = input("HELPER.PY: Head inside NeuraGenix? (HELPER.PY:[yes/no]): ")
                if breakQuery == "yes":
                    print("HELPER.PY: Entering building. ")
                    break
                elif breakQuery == "no":
                    branch2_2 = input("HELPER.PY: What would you like to do?"
                                      "\n(1): Check surroundings"
                                      "\n(2): Locations "
                                      "\n(3): Status "
                                      "\n(4): Move "
                                      "\n "
                                      "\nInput: ")

        #######################################################################################################################
        # Step 3
        while True:
            print("You're stopped by the guards. Flashing your RFID-card, you're given access to the premises."
                  "\nThough they seem wary, they let you through. You're now within the premises.")
            branch2_3 = input("HELPER.PY: What would you like to do? "
                              "\n(1): Check surroundings"
                              "\n(2): Locations "
                              "\n(3): Status "
                              "\n "
                              "\nInput: ")

            if branch2_3 == "1":
                print("Before you is a large lobby. You see an info-desk, waiting area with seats and some bathrooms. ")
                moveOption = input("What would you like to do? "
                                   "\n (1): Info-desk "
                                   "\n (2): Waiting area "
                                   "\n (3): Bathroom ")
                if moveOption == "1":
                    input("Going to the info-desk, you try to chat up the attendant."
                          "\nYou are inquired for your business and contact personnel. ")
                    input("Trying to smooth talk isn't successful. "
                          "\nYou are asked to leave the area before the guards will be alerted.")
                    input("DEBUG: Lose game or penalty here. ")
                    break
                elif moveOption == "2":
                    input("Going to the waiting area, you sit down with a presence. ")
                    input("Waiting a bit, exuding intended presence, you note ignoring other passerby's. ")
                    input("Noting the attendant is busy with transfer calls and paperwork. ")
                    input("You bring out your laptop as if waiting for someone to come pick you up. ")
                    input("You install the usb you were provided. This brings out an remote access panel. ")
                    input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
                    input("USER: K3rn3lGh0$t sent: HEH gotchu now.  (HELPER.PY: [Enter]) ")
                    input(
                        "USER: K3rn3lGh0$t sent: Lmao, don't sweat it. We already had your stuff.  (HELPER.PY: [Enter]) ")

                    input(
                        "USER: K3rn3lGh0$t sent: Anyway, sit back. Don't look stiff, I'll help ya out.  (HELPER.PY: [Enter]) ")
                    input(
                        "-KGRoot.init .\clientConnection:500.6904-676@LogPoint:6784.1245.3455.000.000:  (HELPER.PY: [Enter]) ")
                    input(
                        """ 
                            echo "[INFO] Executing exploit on CVE-2024-1234 - Authentication Bypass Exploit"
                            sleep 2
                            echo "[INFO] Injecting payload..."
                            sleep 3
                            echo "[SUCCESS] Payload injected successfully. Access granted to internal network. "

                            echo "[INFO] Scanning internal network for accessible resources..."
                            sleep 2
                            echo "[INFO] Discovered 3 active servers:"
                            sleep 1
                            echo "      [1] FileServer01 - 192.168.1.10"
                            echo "      [2] DatabaseServer - 192.168.1.20"
                            echo "      [3] MailServer - 192.168.1.30"
                            sleep 1
                            echo "[INFO] Attempting to access DatabaseServer..."
                            sleep 2
                            echo "[SUCCESS] Secure.server access established. -HANDSHAKE- .kg\ForceOpen.exe."
                        """)

                    input(
                        """
                        // Initializing NeuraGenix Biometric Security Bypass
                        >>> Initializing facial recognition bypass...

                        [Scanning NeuraGenix executive database...]
                        [Acquiring facial image dataset...]
                        [Generating 3D facial model... 5%]
                        [Generating 3D facial model... 12%]
                        [Generating 3D facial model... 34%]
                        [Generating 3D facial model... 36%]
                        [Generating 3D facial model... 80%]
                        [Generating 3D facial model... 90%]

                        >>> Facial recognition match: 97% accuracy
                        >>> Status: Bypass successful

                        // Proceeding to voiceprint authentication...
                        >>> Initiating voiceprint data extraction...
                         """)

                    # TASKS HERE

                    input("""
                    [Accessing archived audio files...]
                    [Extracting voice patterns: Frequency, Pitch, Tone...]
                    [Generating synthetic voice model...2%]
                    [Generating synthetic voice model...6%]
                    [Generating synthetic voice model...5%]
                    [Generating synthetic voice model...15%]
                    [Generating synthetic voice model...68%]
                    [Generating synthetic voice model...78%]
                    [Generating synthetic voice model...87%]

                    >>> Voiceprint match: 92% accuracy
                    >>> Status: Bypass successful
                     """)

                    # TASKS HERE

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
                    input("USER: K3rn3lGh0$t sent: Done, got the packet. Rest is on you. (HELPER.PY: [Enter]) ")
                    input(
                        "HELPER.PY: It would be reasonable to exit the premises. You have however raised suspicion. [Enter]")
                    input("HELPER.PY: Your details have been presumably caught by the security cameras. [Enter]")
                    input("HELPER.PY: Before leaving, I suggest scrubbing the data. [Enter]")
                    input("HELPER.PY: Head to the bathroom for injection. [Enter]")
                    input("HELPER.PY: Leave your pc to make it seem natural. Use your phone's remote access. [Enter]")
                    print("You go the bathroom and boot up systemLink. ")
                    input("HELPER.PY: ..\Exfiltration.exe- [Enter]")
                    print(
                        """
                        // Initializing NeuraGenix Security Camera System Bypass
                        >>> Accessing camera feed storage...

                        [Connecting to NeuraGenix security network...]
                        [Bypassing encryption layers...]
                        [Authorization token spoofed]

                        >>> Camera feed access granted
                        >>> Locating relevant video files...

                        [Searching for recent surveillance recordings...]
                        >>> Files located: CAM_12_09-2024.log, CAM_13_09-2024.log, CAM_14_09-2024.log
                        """)

                    # TASKS HERE

                    input("""
                    >>> Initiating file corruption sequence...
                    [Overwriting CAM_12_09-2024.log...]
                    >>> 25% complete...
                    >>> 50% complete...
                    >>> 100% complete - File corrupted
                     """)

                    # TASKS HERE

                    input("""
                    [Overwriting CAM_13_09-2024.log...]
                    >>> 25% complete...
                    >>> 50% complete...
                    >>> 100% complete - File corrupted
                    """)

                    # TASKS HERE

                    input("""
                    [Overwriting CAM_14_09-2024.log...]
                    >>> 25% complete...
                    >>> 50% complete...
                    >>> 100% complete - File corrupted

                    >>> Status: All relevant surveillance footage has been erased.
                    """)

                    # TASKS HERE

                    input("""
                    >>> Initiating log cleanup...

                    [Scrubbing access logs...]
                    >>> Log entries for Camera Access successfully deleted
                    >>> System audit trail: Clean

                    >>> Surveillance bypass complete. No trace detected.
                    """)

                    # TASKS HERE

                    input("You've successfully erased incriminating data. ")
                    input(
                        "Time to head out. Holding a phone in hand and pretending to talk to someone, you leave the premises. ")
                    input("You almost forget your laptop, but that will only help sell the trick. ")
                    input("Picking up your stuff, you head out of the building. ")
                    pay = 1000
                    print(f"Mission completed. Your reward is: {pay}©")
                    # Add pay to player cash amount.

                    break
                elif moveOption == "3":
                    input("You head to the bathroom. ")
                    input("Locking yourself in the stall, you begin your work. ")
                    input("You install the usb you were provided. This brings out an remote access panel. ")
                    input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
                    input("USER: K3rn3lGh0$t sent: HEH gotchu now.  (HELPER.PY: [Enter]) ")
                    input(
                        "USER: K3rn3lGh0$t sent: Lmao, don't sweat it. We already had your stuff.  (HELPER.PY: [Enter]) ")
                    input("USER: K3rn3lGh0$t sent: Anyway, sit back. I'll help ya out. (HELPER.PY: [Enter]) ")
                    input(
                        "-KGRoot.init .\clientConnection:500.6904-676@LogPoint:6784.1245.3455.000.000:  (HELPER.PY: [Enter]) ")
                    input(
                        """ 
                            echo "[INFO] Executing exploit on CVE-2024-1234 - Authentication Bypass Exploit"
                            sleep 2
                            echo "[INFO] Injecting payload..."
                            sleep 3
                            echo "[SUCCESS] Payload injected successfully. Access granted to internal network. "

                            echo "[INFO] Scanning internal network for accessible resources..."
                            sleep 2
                            echo "[INFO] Discovered 3 active servers:"
                            sleep 1
                            echo "      [1] FileServer01 - 192.168.1.10"
                            echo "      [2] DatabaseServer - 192.168.1.20"
                            echo "      [3] MailServer - 192.168.1.30"
                            sleep 1
                            echo "[INFO] Attempting to access DatabaseServer..."
                            sleep 2
                            echo "[SUCCESS] Secure.server access established. -HANDSHAKE- .kg\ForceOpen.exe."
                        """)

                    input(
                        """
                        // Initializing NeuraGenix Biometric Security Bypass
                        >>> Initializing facial recognition bypass...

                        [Scanning NeuraGenix executive database...]
                        [Acquiring facial image dataset...]
                        [Generating 3D facial model... 5%]
                        [Generating 3D facial model... 12%]
                        [Generating 3D facial model... 34%]
                        [Generating 3D facial model... 36%]
                        [Generating 3D facial model... 80%]
                        [Generating 3D facial model... 90%]

                        >>> Facial recognition match: 97% accuracy
                        >>> Status: Bypass successful

                        // Proceeding to voiceprint authentication...
                        >>> Initiating voiceprint data extraction...
                         """)

                    # TASKS HERE

                    input("""
                    [Accessing archived audio files...]
                    [Extracting voice patterns: Frequency, Pitch, Tone...]
                    [Generating synthetic voice model...2%]
                    [Generating synthetic voice model...6%]
                    [Generating synthetic voice model...5%]
                    [Generating synthetic voice model...15%]
                    [Generating synthetic voice model...68%]
                    [Generating synthetic voice model...78%]
                    [Generating synthetic voice model...87%]

                    >>> Voiceprint match: 92% accuracy
                    >>> Status: Bypass successful
                     """)

                    # TASKS HERE

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
                    input("USER: K3rn3lGh0$t sent: Done, got the packet. Rest is on you. (HELPER.PY: [Enter]) ")
                    input(
                        "Time to head out. Holding a phone in hand and pretending to talk to someone, you leave the premises. ")
                    input("By the time you leave the area, you are contacted. ")
                    input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
                    input("USER: Gh0stP@cket sent: yo ***h*l* you forgot to scrub the data. (HELPER.PY:[Enter]): ")
                    input(
                        "USER: Gh0stP@cket sent: we got the prototype-data and backdoor access t2u, but this was a miss. (HELPER.PY:[Enter]): ")
                    input(
                        "USER: Gh0stP@cket sent: we'll mask your entry with a ddos, that way we can remove evidence. (HELPER.PY:[Enter]): ")
                    input(
                        "USER: Gh0stP@cket sent: next time you better do this **** proper. Remember were watching you. (HELPER.PY:[Enter]): ")
                    input("HELPER.PY: Your details have been presumably caught by the security cameras. [Enter]")
                    input("HELPER.PY: We can hope that the organization manages to wipe the slate. [Enter]")
                    input("HELPER.PY: Time to finish here. Awaiting further contact. On standby. [Enter]")
                    pay = 500
                    print(f"Mission completed. Your reward is: {pay}©")
                    # Add pay to player cash amount.
                    break

    #######################################################################################################################


def mission1Tasks():
    points = 0
    randValue = random.randint(1, 4)
    while points < 4:
        if randValue == 1:
            task1 = input("Question: What does GMO stand for in biotechnology?")
            if task1 == "Genetically Modified Organism" or task1 == "genetically modified organism":
                print("Correct! Well done!")
                points += 1
            else:
                print("Incorrect. Try again!")
                raiseThreat("failure")
        elif randValue == 2:
            task2 = input("Question: Which famous biotechnology tool allows for precise editing of DNA sequences?")
            if task2 == "CRISPR" or task2 == "crispr":
                print("Correct! Well done!")
                points += 1
            else:
                print("Incorrect. Try again!")
                raiseThreat("failure")
        elif randValue == 3:
            task3 = input(
                "Question: In which year was the first genetically modified crop, the Flavr Savr tomato, approved for commercial sale in the U.S.? HINT it's in the 90s")
            if task3 == "1994":
                print("Correct! Well done!")
                points += 1
            else:
                print("Incorrect. Try again!")
                raiseThreat("failure")
        elif randValue == 4:
            task4 = input(
                "Question: What is the term for the process of transferring genes from one organism to another?")
            if task4 == "Genetic Engineering" or task4 == "genetic engineering":
                print("Correct! Well done!")
                points += 1
            else:
                print("Incorrect. Try again!")
                raiseThreat("failure")


def mission2():
    # Encryption aiheinen tehtävä
    print("Mission 2")
    input("Cipherium Technologies is reputed to engage in covert operations, "
          "\nusing their cutting-edge encryption to shield corruption and protect dubious corporations from public eye. "
          "\nFind the dirt and reveal it.")

    input("NEW CHAT INBOUND (HELPER.PY:[Enter]) ")
    # input("USER: Gh0stP@cket sent:  (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: good and ready hackerling? (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: our next task is to tackle Cipherium Technologies. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: they deal in encryption to shield dirty corporate secrets. (HELPER.PY:[Enter]): ")
    input(
        "USER: Gh0stP@cket sent: apparently they also do black business practices, extortion and monopoly bs (HELPER.PY:[Enter]): ")
    input(
        "USER: Gh0stP@cket sent: this time its all on you but remember that we in this together. (HELPER.PY:[Enter]): ")

    #######################################################################################################################
    # Step 1
    step1State = 0
    while True:
        if step1State == 1:
            breakQuery = input("HELPER.PY: Would you like to move to Cipherium Tech.? (HELPER.PY:[yes/no]): ")
            if breakQuery == "yes":
                print("HELPER.PY: Moving to target. ")
                break
            elif breakQuery == "no":
                branch2_1 = input("HELPER.PY: What would you like to do?"
                                  "\n(1): Locations "
                                  "\n(2): Web "
                                  "\n(3): Status "
                                  "\n(4): Move "
                                  "\n "
                                  "\nInput: ")
        elif step1State == 0:
            branch2_1 = input("HELPER.PY: What would you like to do?"
                              "\n(1): Locations "
                              "\n(2): Web "
                              "\n(3): Status "
                              # "\n(4): Move "
                              "\n "
                              "\nInput: ")

            if branch2_1 == "1":
                if step1State == 0:
                    # print("HELPER.PY: ")
                    print("HELPER.PY: Current available locations are: "
                          "\n>Home<"
                          "\n ")
                elif step1State == 1:
                    print("HELPER.PY: Current available locations are: "
                          "\n>Home<"
                          "\n*Cipherium"
                          "\n ")
            elif branch2_1 == "2":
                input("WIP: Web content for Cipherium....")
                step1State = 1
                print("State updated."
                      "\n ")
            elif branch2_1 == "3":
                print(f"Your current threat level is: blahblah"
                      f"\n ")
            elif branch2_1 == "4":
                breakQuery = input("HELPER.PY: Would you like to move to Cipherium Tech.? (HELPER.PY:[yes/no]): ")
                if breakQuery == "yes":
                    print("HELPER.PY: Moving to target. ")
                    break
                elif breakQuery == "no":
                    branch2_1 = input("HELPER.PY: What would you like to do?"
                                      "\n(1): Locations "
                                      "\n(2): Web "
                                      "\n(3): Status "
                                      "\n(4): Move "
                                      "\n "
                                      "\nInput: ")


def mission2Tasks():
    points = 0
    randomValue = random.randint(1, 4)
    while points < 4:
        if randomValue == 1:
            task1 = input("Solve the following sentence using Caesar Shift -1: 'fnnc ktbj rzuhmf sgd vnqkc'\n")
            if task1 == "good luck saving the world":
                print("Correct! Well done!")
                points += 1
            else:
                print("Incorrect. Try again!")
                raiseThreat("failure")
        elif randomValue == 2:
            task2 = input("Solve the following word using Caesar Shift -1: 'gnknfqzl'\n")
            if task2 == "hologram":
                print("Correct! Well done!")
                points += 1
            else:
                print("Incorrect. Try again!")
                raiseThreat("failure")
        elif randomValue == 3:
            task3 = input("Solve the following sentence using Caesar Shift -1: 'zqd xnt rdqhntr'\n")
            if task3 == "are you serious":
                print("Correct! Well done!")
                points += 1
            else:
                print("Incorrect. Try again!")
                raiseThreat("failure")
        elif randomValue == 4:
            task4 = input("Solve the following sentence using Caesar Shift -1: 'fnnc lnqmhmf uhdszml'\n")
            if task4 == "good morning vietnam":
                print("Correct! Well done!")
                points += 1
            else:
                print("Incorrect. Try again!")
                raiseThreat("failure")


# FUNKTIOT PÄÄTTYY
########################################################################################################################
# MAIN

# Soitetaan taustamusiikki loopattuna asynkronisesti (ei pysäytä ohjelmaa)
playback = Playback()  # creates an object for managing playback of a single audio file
playback.load_file('bgmusicexample.mp3')
playback.loop_at_end(True)
playback.play()

maat = []
airports = []

player = init()

currentMission = False

websivut = {
    "ghostrepo.net": """
    ghostrepo.net

    Testi
    Testi
    Testi
    """,
    "privaracapital.org": """
    privaracapital.org

    Testi
    testi
    testi
    """
}

# Alustetaan alkuruutu-animaation sisältö monirivisellä tekstillä
alkuanimaatioruutu = """
 ___   _                 _         
|_ _| ( )  _ __ ___     (_)  _ __  
 | |  |/  | '_ ` _ \    | | | '_ \ 
 | |      | | | | | |   | | | | | |
|___|     |_| |_| |_|   |_| |_| |_|
                Hacker on board...


"""

# Häviö animaatio
havioanimaatioruutu = """                                       
    @@@     @@@@@@@@@@@@@@@@@@@@@@@@@     @@@    
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

Epic Cinematic Gaming Cyberpunk | RESET by Alex-Productions | https://onsound.eu/
Music promoted by https://www.chosic.com/free-music/all/
Creative Commons CC BY 3.0
https://creativecommons.org/licenses/by/3.0/
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
lowerThreat()

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
# travel_menu("FI")
# travel_to("EFHK")

# PÄÄOHJELMA
# mission0()
# mission1()
# mission2()
# winGame()
# winScreen()
# endScreen()