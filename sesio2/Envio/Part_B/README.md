# Explicació de les carpetes

Part_A
En aquesta carpeta hi ha tots els fitxers de la primera part de la pràctica.
A abs-info(el conjunt de dades arxiv_abs) ia news-info(20_newsgroups) tenim els resultats que obtenim en indexar amb cada token i filtre que fem servir. El nom de cada fitxer indica el tocken i els filtres que fem servir.
A l'arxiu snowball.out tenim els tokens que els extraiem usant CountWords.py.
El fitxer data_snowball.csv el creem usant filter_words.py de la practica1. D'aquest fitxer usant el ZipfLaw.py(també de la practica1) creem els grfics del Zipf.


Part_B
Fem servir TFIDFViewer.py per calcular la similaritat de cada conjunt de dades. A les carpetes abs-similarity, news-similarity, novels-similarity hi ha els resultats de cada comparacio, a cada fitxer de cada carpeta hi ha els noms de cada arxiu que comparem(ex en similarity a a1 aquesta: arxiv_abs/astro-ph.updates .on.arXiv.org arxiv_abs/cond-mat.updates.on.arXiv.org).


# Instruccions d'execució del programari



Ejemplo de como indexar 20_newsgroups
```shell
python3 IndexFilesPreprocess.py --index news --path 20_newsgroups --token letter --filter lowercase asciifolding snowball stop
```
Ejemplo de como indexar arxiv_abs
```shell
python3 IndexFilesPreprocess.py --index abs --path arxiv_abs --token letter --filter lowercase asciifolding snowball stop
```
Ejemplo de como indexar novels
```shell
python3 IndexFilesPreprocess.py --index novels --path novels --token letter --filter lowercase asciifolding snowball stop
```

Ejemplo de como ejecutar para 20_newsgroups
```shell
python3 TFIDFViewer.py --index news --path 20_newsgroups/alt.atheism 20_newsgroups/sci.space 
```
Ejemplo de como ejecutar para arxiv_abs
```shell
python3 TFIDFViewer.py --index abs --path arxiv_abs/astro-ph.updates.on.arXiv.org arxiv_abs/cond-mat.updates.on.arXiv.org
```
