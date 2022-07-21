FROM aidarms/stream-gait:latest

COPY processor.py ./data_processors/simple_processor/processor.py
COPY run.py ./data_processors/simple_processor/run.py

# Below are the default values
ENV LIMIT 250
ENV SOURCE_TYPE file
ENV SOURCE_NAME labeled_data
ENV DEST_TYPE file
ENV DEST_NAME data.txt
ENV PYTHONPATH ${PYTHONPATH}:.

CMD python data_processors/simple_processor/run.py --record-limit $LIMIT \
        --source-type $SOURCE_TYPE --source-name $SOURCE_NAME \
        --dest-type $DEST_TYPE --dest-name $DEST_NAME