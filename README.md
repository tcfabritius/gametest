# I'm in - Hacker on board

##  1 Tietokantojen asennus

Aja seuraava komento MariaDB komentokehotteella luodaksesi ja tuodaksesi tietokanta:

```
create database flight_game;
exit
mysql -u root -p flight_game < "[polku]/tietokanta.sql"
```

**korvaa [polku] sql tiedoston sijainnilla.**

## 2 Kirjastojen asennus

Seuraavalla komennolla asennetaan vaaditut kirjastot PyCharmin komentokehotteella:
```
pip install -r requirements.txt
```

## 3 Pelin toisto

Peli toistetaan klikkaamalla pycharmissa game.py tiedostoa hiiren oikealla ja Open in->Terminal:

Komennolla:
```
py game.py
```
