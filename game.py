# Tuodaan Decrypt-efekti terminaltekstianimaatioita varten
from terminaltexteffects.effects.effect_decrypt import Decrypt

# Tuodaan Matrix-efekti terminaltekstianimaatioita varten
from terminaltexteffects.effects.effect_matrix import Matrix

# Tuodaan Burn-efekti terminaltextanimaatiota varten
from terminaltexteffects.effects.effect_burn import Burn

# Tuodaan Burn-efekti terminaltextanimaatiota varten
from terminaltexteffects.effects.effect_fireworks import Fireworks

# Tuodaan Fore ja Style väritekstejä varten
from colorama import (Fore, Style)

# Tuodaan just_playback äänentoistoa varten
from just_playback import Playback

# Tuodaan os ruuduntyhjennystä varten
import os

import mysql.connector
from geopy import distance

def clear_console():
    # For Windows, use 'cls', for Mac/Linux, use 'clear'
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS and Linux
        os.system('clear')

def alkuruutu():
    # Luodaan Decrypt-efekti alkuruudun animaatiota varten
    effect = Decrypt(alkuanimaatioruutu)
    effect.effect_config.merge = True  # Määritetään, että animaatioiden kehykset sulautuvat yhteen

    # Animaatio toistetaan terminaaliin
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

    tmp = input("Press enter to continue")
    clear_console()

def häviöruutu():
    # Luodaan Burn-efekti alkuruudun animaatiota varten
    effect = Burn(havioanimaatioruutu)
    effect.effect_config.merge = True  # Määritetään, että animaatioiden kehykset sulautuvat yhteen

    # Animaatio toistetaan terminaaliin
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

    tmp = input("Press enter to continue...")

    clear_console()

def voittoruutu():
    # Luodaan Fireworks-efekti voittoruudun animaatiota varten
    effect = Fireworks(voittoanimaatioruutu)

    # Animaatio toistetaan terminaaliin
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

    tmp = input("Press enter to continue...")

    clear_console()

def loppuruutu():
    # Luodaan Matrix-efekti loppuruudun animaatiota varten
    effect = Matrix(loppuanimaatioruutu)

    # Animaatio toistetaan terminaaliin
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

def web(mission_id):
    clear_console()
    cursor.execute("SELECT description FROM mission WHERE id = %s", (mission_id))
    connection.commit()
    kuvaus = cursor.fetchall()
    print(Fore.GREEN + kuvaus[1])
    tmp = input("Press enter to exit web browser")
    clear_console()

connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='user',
         password='user',
         autocommit=True
         )


# Alustetaan alkuruutu-animaation sisältö monirivisellä tekstillä
alkuanimaatioruutu = """
 ___   _                 _         
|_ _| ( )  _ __ ___     (_)  _ __  
 | |  |/  | '_ ` _ \    | | | '_ \ 
 | |      | | | | | |   | | | | | |
|___|     |_| |_| |_|   |_| |_| |_|
 _   _            _                             _                         _ 
| | | | __ _  ___| | _____ _ __    ___  _ __   | |__   ___   __ _ _ __ __| |
| |_| |/ _` |/ __| |/ / _ \ '__|  / _ \| '_ \  | '_ \ / _ \ / _` | '__/ _` |
|  _  | (_| | (__|   <  __/ |    | (_) | | | | | |_) | (_) | (_| | | | (_| |
|_| |_|\__,_|\___|_|\_\___|_|     \___/|_| |_| |_.__/ \___/ \__,_|_|  \__,_|
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

#havioanimaatioruutu = """
#                                     @@@@@@@@@@@@@@@@@@@@@@@@@@
#                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                    @@@@@@@@@@@@@@@@@     @@@@@@@@@@@@@@@@     @@@@@@@@@@@@@@@@
#                     @@@@@@@@@               @@@@@@@@@                @@@@@@@@
#                       @@@@@@                 @@@@@@@@                @@@@@@
#                         @@@@@             @@@@@@@@@@@@@@             @@@@@
#                        @@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@
#                       @@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@@@@
#                                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                 @@@@@@@              @@@@@@@@@@@@@@@@@@@@@@@@              @@@@@@@
#               @@@@@@@@@@@           @@@@@@@@@@@@@@@@@@@@@@@@@@           @@@@@@@@@@@
#               @@@@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@           @@@@@@@@@@@@@
#           @@@@@@@@@@@@@@@@@@@@@                                    @@@@@@@@@@@@@@@@@@@@@
#          @@@@@@@@@@@@@@@@@@@@@@@@@@@@                       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#            @@@@@@@@@      @@@@@@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@@@@@      @@@@@@@@@
#                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@
#                                      @@@@@@@@@@@@@@@@@@@@@@@@
#            @@@@@@@@        @@@@@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@@       @@@@@@@@
#          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#           @@@@@@@@@@@@@@@@@@@@@@                                  @@@@@@@@@@@@@@@@@@@@@@
#               @@@@@@@@@@@@@                                            @@@@@@@@@@@@@
#               @@@@@@@@@@@                                               @@@@@@@@@@@@
#                @@@@@@@@                                                   @@@@@@@@@
#"""



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
#winsound.PlaySound("bgmusicexample.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
#playsound.playsound("bgmusicexample.mp3",False)
playback = Playback() # creates an object for managing playback of a single audio file
playback.load_file('bgmusicexample.mp3')
playback.loop_at_end(True)
playback.play()

#alkuruutu()

# Tulostetaan värejä terminaaliin
print(Fore.RED + "Red")  # Tulostetaan punainen teksti
print(Fore.GREEN + "Green")  # Tulostetaan vihreä teksti
print(Fore.BLUE + "Blue")  # Tulostetaan sininen teksti
print(Fore.YELLOW + "Yellow")  # Tulostetaan keltainen teksti
print(Fore.MAGENTA + "Magenta")  # Tulostetaan magenta teksti
print(Fore.CYAN + "Cyan")  # Tulostetaan syaani teksti

# Resetoidaan värimuutokset
print(Style.RESET_ALL)

# Odotetaan käyttäjän syötettä jatkamiseen
tmp = input("Press enter to continue...")

# Ruuduntyhjennys
clear_console()

#häviöruutu()

#loppuruutu()

#Mikon työtila

#Jonin työtila


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



#Outin työtila

