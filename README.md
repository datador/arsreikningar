# Sjálfvirkir Ársreikningar
Skrifta til að sækja íslenska ársreikninga sjálfvirkt út frá breytum eins og Kennitölu og ári.

## Uppsetning

Klóna reposið:
```
git clone https://github.com/datador/arsreikningar.git
```

Fara inn í projectið:
```
cd arsreikningar
```

Install á dependencies (Mæli með að nota environment, t.d. venv eða conda):
```
pip install -r requirements.txt
```

## Notkun

Skriftan er síðan keyrð:

```
python main.py --ssn_list KENNITALA_1 KENNITALA_2 ... KENNITALA_N 
```

### Breytur

`--ssn_list`: kennitala/tölur aðskildar með bili (required).

`--start_year`: upphafsár sem skriftan sækir, ef ekkert er tilgreint er default á "None" sem tekur nýjasta ársreikninginn stakann (default: `None`).

`--path`: Absolute path til þess að skila gögnunum í, defaultast á rót/data (default: `./data`).

`--unzip`: Boolean gildi til að unzippa, skilgreina þarf með false ef ekki á að unzippa (default: `true`).

### Dæmi

```
python main.py --ssn_list 1234567890

python main.py --ssn_list 1234567890 0987654321 --path C:/arsreikningar/data --unzip false

python main.py --ssn_list 1234567890 0987654321 --start_year 2020 --path C:/arsreikningar/data --unzip true
```

## Docker

Einnig er hægt að keyra skriftuna í container með eftirfarandi hætti:

### Byggja image

```
docker build -t arsrkn .
```

### Keyra gáma út frá image

Þar sem skriftan skilar gögnum þarf að mounta eitthvað path á viðeigandi stað, ef ársreikningarnir eiga að skila sér út úr gámnum..

Hægt er síðan að keyra upp marga gáma með mismunandi parametra.. Breyta þarf "Path/fyrir/data" í eitthvað viðegandi, t.d. C:/arsreikningar
```
docker run -d -v Path/fyrir/data:/app/data --name arsrkn-container arsrkn --ssn_list 4910080160 6312051780 --start_year 2020 --unzip True
```

### Ná í logga úr gámnum

```
docker logs arsrkn-container
```

### Stoppa og eyða gámum

```
docker stop arsrkn-container
docker rm arsrkn-container
```

## Strúktúr

```
arsreikningar/
├── data/
├── src/
│ ├── __init__.py
│ ├── web_setup.py
│ ├── utils.py
├── main.py
├── requirements.txt
├── Dockerfile
├── README.md
```

## Skrár

`main.py`: keyrir allt saman

`src/web_setup.py`: Heldur utanum Selenium WebDriver uppsetningu.

`src/utils.py`: Utility föll

`requirements.txt`: Heldur utan um hvaða pakka þarf að ná í til að keyra.

`Dockerfile`: Skilgreinir uppskrift að "Docker image" fyrir öll dependency.

`README.md`: Howto og core upplýsingar