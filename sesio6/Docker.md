We first run the docker service
```sh
systemctl start docker
```

Now we run our container with the elasticsearch image
```sh
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.17.7
```
