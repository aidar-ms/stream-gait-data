#! /bin/zsh

docker exec -ti broker kafka-topics --bootstrap-server=localhost:9092 --list