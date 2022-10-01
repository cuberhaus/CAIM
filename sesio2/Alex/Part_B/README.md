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
