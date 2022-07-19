#! /bin/sh


docker exec -ti broker kafka-topics --bootstrap-server=localhost:9092 --topic $1 --delete