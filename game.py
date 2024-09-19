# Tuodaan Decrypt-efekti terminaltekstianimaatioita varten
from terminaltexteffects.effects.effect_decrypt import Decrypt

# Tuodaan Matrix-efekti terminaltekstianimaatioita varten
from terminaltexteffects.effects.effect_matrix import Matrix

# Tuodaan Fore ja Style väritekstejä varten
from colorama import Fore, Style

# Tuodaan winsound äänentoistoa varten
import winsound

# Alustetaan alkuruutu-animaation sisältö monirivisellä tekstillä
alkuanimaatioruutu = """
 ___ _             ___       
|_ _( )_ __ ___   |_ _|_ __  
 | ||/| '_ ` _ \   | || '_ \ 
 | |  | | | | | |  | || | | |
|___| |_| |_| |_| |___|_| |_|
              Hacker on board
"""

# Alustetaan loppuruutu-animaation sisältö monirivisellä tekstillä
loppuanimaatioruutu = """
Epic Cinematic Gaming Cyberpunk | RESET by Alex-Productions | https://onsound.eu/
Music promoted by https://www.chosic.com/free-music/all/
Creative Commons CC BY 3.0
https://creativecommons.org/licenses/by/3.0/
"""

# Soitetaan taustamusiikki loopattuna asynkronisesti (ei pysäytä ohjelmaa)
winsound.PlaySound("bgmusicexample.wav", winsound.SND_LOOP + winsound.SND_ASYNC)

# Luodaan Slide-efekti alkuruudun animaatiota varten
effect = Decrypt(alkuanimaatioruutu)
effect.effect_config.merge = True  # Määritetään, että animaatioiden kehykset sulautuvat yhteen

# Animaatio toistetaan terminaaliin
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin

# Tulostetaan värejä terminaaliin
print(Fore.RED + "Red")      # Tulostetaan punainen teksti
print(Fore.GREEN + "Green")  # Tulostetaan vihreä teksti
print(Fore.BLUE + "Blue")    # Tulostetaan sininen teksti
print(Fore.YELLOW + "Yellow")# Tulostetaan keltainen teksti
print(Fore.MAGENTA + "Magenta") # Tulostetaan magenta teksti
print(Fore.CYAN + "Cyan")    # Tulostetaan syaani teksti

# Resetoidaan värimuutokset
print(Style.RESET_ALL)

# Odotetaan käyttäjän syötettä jatkamiseen
tmp = input("Press enter to continue...")

# Luodaan Beams-efekti loppuruudun animaatiota varten
effect = Matrix(loppuanimaatioruutu)

# Animaatio toistetaan terminaaliin
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin
