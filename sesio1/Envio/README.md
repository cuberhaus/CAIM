# Instruccions d'execució del programari
## ZipfLaw

Primer generem mitjançant l'script CountWords.py els fitxers de dades .txt. Després executem el programa filter_words.py (amb el flag --path indiquem el fitxer que volem fer servir) que ens filtrarà les paraules i les col·locarà en un arxiu en format csv.
```shell
python3 filter_words.py --path words_nov.txt (archiu de les dades acabat amb extensió txt)
```
Tot seguit executarem el programa ZipfLaw.py(amb el flag --path indiquem el fitxer que volem fer servir) que ens crearà uns gràfics amb els resultats corresponents.
```shell
python3 ZipfLaw.py --path data_novels.csv (sempre un fitxer amb extensió csv)
```
## HeapLaw
Per a executar el Heap primer hem d'indexar les noveles amb:
```sh
python3 Split_and_Index_Novels.py
```
Després executem el codi HeapLaw.py que ens crearà unes gràfiques amb els resultats.
```sh
python3 HeapLaw.py
```
