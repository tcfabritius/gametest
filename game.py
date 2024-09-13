# Tuodaan Slide-efekti terminaltekstianimaatioita varten
from terminaltexteffects.effects.effect_slide import Slide

# Tuodaan Beams-efekti terminaltekstianimaatioita varten
from terminaltexteffects.effects.effect_beams import Beams

# Tuodaan Fore ja Style väritekstejä varten
from colorama import Fore, Style

# Tuodaan winsound äänentoistoa varten
import winsound

# Alustetaan alkuruutu-animaation sisältö monirivisellä tekstillä
alkuanimaatioruutu = """
  ___ ___          .__   .__               
 /   |   \   ____  |  |  |  |    ____      
/    ~    \_/ __ \ |  |  |  |   /  _ \     
\    Y    /\  ___/ |  |__|  |__(  <_> )    
 \___|_  /  \___  >|____/|____/ \____/     
       \/       \/                         

 __      __               .__       .___._.
/  \    /  \ ____ _______ |  |    __| _/| |
\   \/\/   //  _ \\_  __ \|  |   / __ | | |
 \        /(  <_> )|  | \/|  |__/ /_/ |  \|
  \__/\  /  \____/ |__|   |____/\____ |  __
       \/                            \/  \/
"""

# Alustetaan loppuruutu-animaation sisältö monirivisellä tekstillä
loppuanimaatioruutu = """
Epic Cinematic Gaming Cyberpunk | RESET by Alex-Productions | https://onsound.eu/
Music promoted by https://www.chosic.com/free-music/all/
Creative Commons CC BY 3.0
https://creativecommons.org/licenses/by/3.0/

Sound Effect by UNIVERSFIELD from Pixabay
https://pixabay.com/users/universfield-28281460/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=144751
https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=144751
"""

# Soitetaan taustamusiikki loopattuna asynkronisesti (ei pysäytä ohjelmaa)
winsound.PlaySound("bgmusicexample.wav", winsound.SND_LOOP + winsound.SND_ASYNC)

# Luodaan Slide-efekti alkuruudun animaatiota varten
effect = Slide(alkuanimaatioruutu)
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
effect = Beams(loppuanimaatioruutu)

# Animaatio toistetaan terminaaliin
with effect.terminal_output() as terminal:
    for frame in effect:
        terminal.print(frame)  # Tulostetaan animaation kukin kehys terminaaliin
