## Wejście na platformę w trybie online

W tym przypadku wystarczy wejść na **www.platformajm.pl**
Platforma nie posiada certyfikatu **SSL**, gdyż jest to tylko prototyp do testów online.
## Włączenie platformy w trybie offline

Wymagana wersja python: **3.11**
Wymagany **nodeJS**

`pip install -r requirements.txt`
`cd .\frontend\sign-recognition-project\`
`npm install`

Po poprawnym zainstalowaniu bibliotek python oraz nodejs, możemy uruchomić aplikację.
Wracamy do głównego folderu projektu `cd ../..`
W jednym terminalu uruchamiamy skrypt `./api_start.bat` - uruchomi on REST API (Flask)
W drugim terminalu uruchamiamy skrypt `./website_start.bat` - uruchomi on aplikację vue.js
Po tym możemy wejść na stronę **http://localhost:5173/**, na której mamy w pełni dostępną aplikację.


## Włączenie deweloperskiej części platformy
> Jest ona wyłącznie przydatna do dodawania nowych znaków i testowania na żywo wykrywalności obecnych.
> 
`cd backend`
`python app.py`

Otworzy nam się podgląd z kamery.
Wciskając przycisk **R** przechodzimy do trybu nagrywania

Gdy jesteśmy w tryie nagrywania, wciśnięcie cyfry spowoduje rozpoczęcie robienia 400 zdjęć (do zmiany w pliku `config/constants/py` -> **PHOTO_ITERATIONS**, trwa to około **20 sekund**

Aby sprawdzić jakie oznaczenie będzie miał nasz kolejny gest możemy skorzystać z pliku 
`model/point_recognizer/poin_recognizer_labels.csv`
Przykład pliku:
`1. A` (0)
`2. B` (1)
`3. C` (2)
to jako że numerujemy od zera to nasz kolejny znak będzie miał oznaczenie (**3**)
> Gdybyśmy chcieli nagrywać znak o numerze np 15, to wystarczy w tybie nagrywania nacisńąć jeszcze raz **R**, a do wciśniętej cyfry zostanie dodane 10 podczas zapisu do pliku.

Po nagraniu gestów, które chcieliśmy, punkty zapisane z wykrycia dłoni znajdują się w pliku 
`model/point_recognizer/points.csv`
W tym momencie wykaz punktów, które nagraliśmy jest gotowy do trenowania.

Wystarczy uruchomić skrypt `python train.py` znajdujący się w `/backend/`

Po tym, w folderze `/backend/model/point_recognizer/test_models` będzie znajdował się plik 
**test_point_recognizer.tflite** i jeśli wyniki nauczania nam się podobają, możemy go przekopiować do folderu `/backend/model/point_recognizer` gdzie będzie on używany przez aplikację.
