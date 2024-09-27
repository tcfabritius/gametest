# Tuodaan kirjastot
from terminaltexteffects.effects.effect_decrypt import Decrypt
from terminaltexteffects.effects.effect_matrix import Matrix
from terminaltexteffects.effects.effect_burn import Burn
from terminaltexteffects.effects.effect_fireworks import Fireworks
from colorama import (Fore, Style)
from just_playback import Playback
from geopy import distance
import os
import mysql.connector
import random

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

def endScreen():
    # Luodaan Matrix-efekti loppuruudun animaatiota varten
    effect = Matrix(loppuanimaatioruutu)

    # Animaatio toistetaan terminaaliin
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

def calcPrice(icao1, icao2):
    sql_kysely = f"money from game where id = '{player}'"
    kursori = connection.cursor()
    kursori.execute(sql_kysely)
    saldo = kursori.fetchall()
    sql_kysely = f"select latitude_deg, longitude_deg from airport where ident = '{icao1}'"
    kursori = connection.cursor()
    kursori.execute(sql_kysely)
    sijainti1 = kursori.fetchall()
    sql_kysely = f"select latitude_deg, longitude_deg from airport where ident = '{icao2}'"
    kursori = connection.cursor()
    kursori.execute(sql_kysely)
    sijainti2 = kursori.fetchall()
    hinta = int(distance.distance(sijainti1, sijainti2).km)*1
    if hinta > saldo[0]:
        loseGame()
    return hinta

def raiseThreat(type):
    cursor = connection.cursor()
    cursor.execute("SELECT threat FROM game WHERE id = %s", (player))
    threat = cursor.fetchone()
    if type == "stay":
        if threat + 1 > 100:
            loseGame()
        else:
            cursor.execute("UPDATE threat SET threat = threat +1")
            connection.commit()

    if type == "failure":
        if threat + 3 > 100:
            loseGame()
        else:
            cursor.execute("UPDATE threat SET threat = threat +3")
            connection.commit()

    cursor.close()
    connection.close()

def lowerThreat():
    cursor = connection.cursor()
    cursor.execute("UPDATE threat SET threat = threat - 20")
    connection.commit()
    cursor.close()
    connection.close()

def calcCO2(icao1, icao2):
    sql_kysely = f"select latitude_deg, longitude_deg from airport where ident = '{icao1}'"
    kursori = connection.cursor()
    kursori.execute(sql_kysely)
    sijainti1 = kursori.fetchall()
    sql_kysely = f"select latitude_deg, longitude_deg from airport where ident = '{icao2}'"
    kursori = connection.cursor()
    kursori.execute(sql_kysely)
    sijainti2 = kursori.fetchall()
    valimatka = int(distance.distance(sijainti1, sijainti2).km)
    if valimatka < 1500:
        paastot = valimatka * 225
    else:
        paastot = valimatka * 120
    return paastot

def openWeb(webpage):
    clear_console()
    print("")
    print(Fore.GREEN + websivut[webpage])
    tmp = input("Press enter to exit web browser")
    print(Style.RESET_ALL)
    clear_console()

def loseGame(player):
    # ENDSCREEN NÄKYMÄ (GAME OVER) FAILURE
    print("GAME OVER")

    # Luodaan kursori
    cursor = connection.cursor()
    # Tulostetaan lopullinen CO2 mikä jäi käyttämättä
    CO2Left = cursor.execute("SELECT co2_budget FROM game WHERE id = %s", (player,))
    connection.commit()
    print("CO2 left in the budget: " + CO2Left + "ppm")
    # Tulostetaan käytetty CO2. Luultavasti tarpeeton, ellei pelissä saa CO2 bonuksia.
    totalUsedCO2 = cursor.execute("SELECT co2_consumed FROM game WHERE id = %s", (player,))
    connection.commit()
    print("Total used CO2: " + totalUsedCO2 + "ppm")
    # Tulostetaan jäänyt rahamäärä
    moneyLeft = cursor.execute("SELECT money FROM game WHERE id = %s", (player,))
    connection.commit()
    print("Money left in the budget: " + moneyLeft + "€")
    # Suljetaan kursori ja yhteys
    cursor.close()
    connection.close()

    goBack = input("Press Enter to go back to Main Menu: ")
    if goBack == "":
        openPauseMenu()
    return

def winGame(player):
    # ENDSCREEN NÄKYMÄ (WINSTATE) GREAT SUCCESS!
    print("CONGRATULATIONS FOR WINNING THE GAME!")

    # Luodaan kursori
    cursor = connection.cursor()
    # Tulostetaan lopullinen CO2 mikä jäi käyttämättä
    CO2Left = cursor.execute("SELECT co2_budget FROM game WHERE id = %s", (player,))
    connection.commit()
    print("CO2 left in the budget: " + CO2Left + "ppm")
    # Tulostetaan käytetty CO2. Luultavasti tarpeeton, ellei pelissä saa CO2 bonuksia.
    totalUsedCO2 = cursor.execute("SELECT co2_consumed FROM game WHERE id = %s", (player,))
    connection.commit()
    print("Total used CO2: " + totalUsedCO2 + "ppm")
    # Tulostetaan jäänyt rahamäärä
    moneyLeft = cursor.execute("SELECT money FROM game WHERE id = %s", (player,))
    connection.commit()
    print("Money left in the budget: " + moneyLeft + "€")
    # Suljetaan kursori ja yhteys
    cursor.close()
    connection.close()

    print("THANK YOU FOR PLAYING THE GAME!\nCREDITS:\nTim Fabritius\nMikko Laakkonen\nJoni Oksanen\nOuti Salonen")

    goBack = input("Press Enter to go back to Main Menu: ")
    if goBack == "":
        openPauseMenu()
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
        openPauseMenu()

def openShop():
    print("Kauppa")

def openPauseMenu():
    print("Pause Menu")

    # PELAAJAN NIMEN KYSYMINEN JA ALKUTIETOJEN ASETTELU. AIKAISEMMAN PELAAJAN TUNNISTAMINEN

def init(connection):

    # Kysytään pelaajan nimi
    print("HACKING USER ID DATABASE...\nACCESS GRANTED...")
    player = input("USE ALIAS: ")

    # Luodaan kursori
    cursor = connection.cursor()

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
        cursor.execute("UPDATE game SET location = %s WHERE id = %s", ('EFHK', player))
        connection.commit()

        # Annetaan uudelle pelaajalle lähtötiedot
        cursor.execute("UPDATE game SET co2_consumed = %s WHERE id = %s", (0, player))
        cursor.execute("UPDATE game SET co2_budget = %s WHERE id = %s", (1000, player))
        cursor.execute("UPDATE game SET money = %s WHERE id = %s", (1000, player))
        connection.commit()

    # Suljetaan kursori ja yhteys
    cursor.close()
    connection.close()

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

    input("HELPER.PY: You probably want to follow the lead on the web. Check: privaraCapital.org on the web. (HELPER.PY:[Enter]): ")

    #Player goes to website - learns more about going to web for info.
    print("YOU: privaraCapital.org")
    # We might need an active message display somewhere after all(?)
    input("HELPER.PY: Username ghostpacket wanted you to infiltrate their crm and internal cashflow via an atm.(HELPER.PY:[Enter]): ")

    print("YOU: Option 3 - Become a client at Privara")

    #Fake bank fake account
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

    #Player will do one mission task here.
    while True:
        firstTask = input("access_point 20: int2**3*int5\nCaseFalse =? ")
        if firstTask == "yes" or "true":
            print("ERROR: Critical user error.")
        elif firstTask == "no" or "false":
            correctAnswer = int(input("Please input correct variable: "))
            if correctAnswer == 40:
                print("access_point 20: STATUS: GREEN")
                break


    #Teach about the threat-mechanic via intrusion
    print("HELPER.PY: /!\WARNING/!\: Threat-level increased.\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")
    #Here is where we update the threat level for the first time.

    #Player goes home
    print("HELPER.PY: Going home...")

    input("USER: Gh0stP@cket sent: bit sloppy but you did the trick (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: package in money out, nice work (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: ill vouch for you, welcome aboard newbie. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: if youre wandering about the bank you just broke into... (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: bunch of cashgrabbers and ******* scam-artists. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: t2u theyre going to be sorting through their **** for a while. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: that and K3rn3lGh0$t injectors. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: anyway, now thats done. Time to move on to bigger fish. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: this world is full of rot and we were needing some new blood. (HELPER.PY:[Enter]): ")
    input("USER: Gh0stP@cket sent: get out there. (HELPER.PY:[Enter]): ")
    print(f"(HELPER.PY:[Enter]): Guided mission protocol over. Good luck {player}")
    print(Style.RESET_ALL)


# Biotech aiheinen tehtävä
def mission1():
    print("Mission 1")

    points = 0

    while points < 4:
        task1 = input("Question: What does GMO stand for in biotechnology?")
        if task1 == "Genetically Modified Organism" or task1 == "genetically modified organism":
            print("Correct! Well done!")
            points += 1
        else:
            print("Incorrect. Try again!")
            raiseThreat("failure")

        task2 = input("Question: Which famous biotechnology tool allows for precise editing of DNA sequences?")
        if task2 == "CRISPR" or task2 == "crispr":
            print("Correct! Well done!")
            points += 1
        else:
            print("Incorrect. Try again!")
            raiseThreat("failure")

        task3 = input("Question: In which year was the first genetically modified crop, the Flavr Savr tomato, approved for commercial sale in the U.S.? HINT it's in the 90s")
        if task3 == "1994":
            print("Correct! Well done!")
            points += 1
        else:
            print("Incorrect. Try again!")
            raiseThreat("failure")


        task4 = input("Question: What is the term for the process of transferring genes from one organism to another?")
        if task4 == "Genetic Engineering" or task4 == "genetic engineering":
            print("Correct! Well done!")
            points += 1
        else:
            print("Incorrect. Try again!")
            raiseThreat("failure")


# Encryption aiheinen tehtävä
def mission2():
    print("Mission 2")

    points = 0

    while points < 4:
        task1 = input("Solve the following sentence using Caesar Shift -1: 'fnnc ktbj rzuhmf sgd vnqkc'\n")
        if task1 == "good luck saving the world":
            print("Correct! Well done!")
            points += 1
        else:
            print("Incorrect. Try again!")
            raiseThreat("failure")

        task2 = input("Solve the following word using Caesar Shift -1: 'gnknfqzl'\n")
        if task2 == "hologram":
            print("Correct! Well done!")
            points += 1
        else:
            print("Incorrect. Try again!")
            raiseThreat("failure")

        task3= input("Solve the following sentence using Caesar Shift -1: 'zqd xnt rdqhntr'\n")
        if task3 == "are you serious":
            print("Correct! Well done!")
            points += 1
        else:
            print("Incorrect. Try again!")
            raiseThreat("failure")

        task4= input("Solve the following sentence using Caesar Shift -1: 'fnnc lnqmhmf uhdszml'\n")
        if task4 == "good morning vietnam":
            print("Correct! Well done!")
            points += 1
        else:
            print("Incorrect. Try again!")
            raiseThreat("failure")









# FUNKTIOT PÄÄTTYY


connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='user',
         password='user',
         autocommit=True
         )

# Soitetaan taustamusiikki loopattuna asynkronisesti (ei pysäytä ohjelmaa)
playback = Playback() # creates an object for managing playback of a single audio file
playback.load_file('bgmusicexample.mp3')
playback.loop_at_end(True)
playback.play()

player = init(connection)

currentMission = False

websivut = {
    "ghostrepo.net":"""
    ghostrepo.net
    
    Testi
    Testi
    Testi
    """,
    "privaracapital.org":"""
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
   @@@        @@@@@@@@@@@@@@@@@@@@@        @@@  
 @@@@@@     @@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@
 @@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@
    @@@@  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@   
      @@@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@     
        @ @@@        @@@@@@@        @@@ @       
          @@    .    @@@@@@@   .     @@         
         @@@@       @@@@ @@@@       @@@@        
         @@@@@@@@@@@@@@   @@@@@@@@@@@@@@        
          @@@ @@@@@@@@@@@@@@@@@@@@@ @@@         
             @ @@@ @@ @@ @@ @@ @@@ @            
       @@@@  @@  youl os ehaha a  @@ @@@@       
   @@@@@@@   @@ @@ @@ @@ @@ @@ @@ @@  @@@@@@@   
   @@@@@@     @@@@@@@@@@@@@@@@@@@@@    @@@@@@   
     @@@       @@@@@@@@@@@@@@@@@@@      @@@      
"""

voittoanimaatioruutu = """
....................... .....
............................ 
..............@@.............
..............@............. 
.@...... .....@...... .... @.
.@.....@@.....@+....@@.  ..@.
..@:.........:@@....@.....@. 
...@#...@@...@@@...@@..  @@..
...@@@..@@@@@@@@@@@@@%.@@@.. 
.. .@@@@@@@@@@@@@@@@@@@@@.. .
....@@@@@@@@@@@@@@@@@@@@@....
  .. ...@@@#..  .:@@@@...  . 
......@@........ ....@@#.....
............................ 
....................... .....
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

#TIMIN FUNKTIOT
#startScreen()
#loseScreen()
#endScreen()
#winScreen()
#openWeb("ghostrepo.net")

#MIKON FUNKTIOT
#mission0()

#JONIN FUNKTIOT
#init()
#loseTheGame()
#winGame()
#optionMenu()

#Svetlanan funktiot

#PÄÄOHJELMA
mission0()
#mission1()
#mission2()
#winGame()
#winScreen()