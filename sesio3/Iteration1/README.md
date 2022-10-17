# Instruccions d'execució del programari


A la carpeta 1.Document_Relevance es troben els resultats de les tres queries de la primera part de la pràctica.
A la carpeta Experiments hi ha tots els experiments que hem fet amb l'algorisme de Rocchio.Hi ha una carpeta per a cadascun dels 8 experiments(abs,Alfa,Beta,Initial,K,novels,nrounds,R).


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

Exemple de com executar Rocchio.py per 20_newsgroups
```shell
python3 Rocchio.py --index news --alpha 1.0 --beta 0.7 --nhits 5 -R 5 --nrounds 5 --query computer windows 
```
Exemple de com executar Rocchio.py per arxiv_abs
```shell
python3 Rocchio.py --index abs --alpha 0.6 --beta 0.6 --nhits 10 -R 3 --nrounds 10 --query computer windows 
```
Exemple de com executar Rocchio.py per novels
```shell
python3 Rocchio.py --index novels --alpha 0.6 --beta 0.6 --nhits 10 -R 3 --nrounds 10 --query computer windows
```
