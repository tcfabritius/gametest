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

def openWeb(webpage):
    clear_console()
    print("")
    print(Fore.GREEN + websivut[webpage])
    tmp = input("Press enter to exit web browser")
    print(Style.RESET_ALL)
    clear_console()

def generateBankKey():
    key = random.randint(1000, 9999)  # Luo satunnaisen 4-numeroisen avaintunnuksen
    return key

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
        if currentMission == success:
            winMission(0)
        elif currentMission == failure:
            loseTheGame()
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
    #Description
    print(Fore.GREEN + """
    Mission Brief: "Infiltration of Privara Capital"
    
    You’ve been recruited by a hacker organization for a critical operation. 
    Your first task is to infiltrate Privara Capital, a bank notorious for its aggressive profit-driven practices. 
    The organization suspects the bank of engaging in illegal activities and needs solid evidence.
    
    Your mission is to breach the bank’s internal network, gather sensitive data, and drive funds to the organization. 
    You'll be equipped with the organization’s custom-built hacking tools.
    
    Good luck —this is your first step into a larger world of high-stakes infiltration.
    """)
    player = input("Enter id: ")

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
    newPrivaraKey = generateBankKey()
    print(f"Your 4-digit key is: {newPrivaraKey}")
    newPrivaraPassword = input("Please input new password: ")
    print("Password set.")
    input("HELPER.PY: Please take mental note of these credentials. (HELPER.PY:[Enter]): ")

    #Might be worth it to utilize some kind of fake code language to do context sensitive actions?
    #Player buys rootkit-device
    print("HELPER.PY: How can I help?")

    print("YOU: Buy rootkit")
    #Lose money

    print("OPTIONS: (1) atm\n(2) customer service\n(3) bathroom")

    print("YOU: OPTION: (1) atm")

    privaraKey = input(f"Please input your 4-letter id: ")
    privaraPassword = input(f"Please input your password: ")
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
    ##2
    intTask2 = input("access_point 20: int2**3*int5\nCaseFalse =? ")
    if intTask2 == "false" or intTask2 == "no":
        correctAnswer = input("input correct variable: ")
        if correctAnswer == 40:
            print("access point status:'PASS'")
            print("out_undo_partial_alloc: while (--i >= 0) {free_page((unsigned long)group_info->blocks[i])};\n"
                    "kfree(group_info); return NULL;) EXPORT_SYMBOL(groups_alloc);")
        # taskScore += 1
        # new task unless matched score is met.
        elif intTask2 == "true" or intTask2 == "yes":
            print("access point status: 'FAILURE'")
            # new task unless matched score is met.
            # refresh new task.
            # add point to threat?
        else:
            print("access point encountered critical user error.")
            print("access point status: 'FAILURE'")
            # refresh new task
            # add point to threat?
    else:
        print("access point encountered critical user error.")
        print("access point status: 'FAILURE'")
        # refresh new task
        # add point to threat?

    #Teach about the threat-mechanic via intrusion
    print("HELPER.PY: /!\WARNING/!\: Threat-level increased.\nPlease consider aborting current mission. (HELPER.PY:[Enter]): ")
    #Here is where we update the threat level for the first time.

    print("HELPER.PY: How can I help?")
    goToLocation = input("YOU: GO_TO: (HELPER.PY:[Home?]): ")

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

# FUNKTIOT PÄÄTTYY


connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='user',
         password='user',
         autocommit=True
         )

player = init(connection)

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

# Soitetaan taustamusiikki loopattuna asynkronisesti (ei pysäytä ohjelmaa)
playback = Playback() # creates an object for managing playback of a single audio file
playback.load_file('bgmusicexample.mp3')
playback.loop_at_end(True)
playback.play()

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

#PÄÄOHJELMA
#init()
#mission0()