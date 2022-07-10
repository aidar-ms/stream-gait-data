FROM aidarms/stream-gait:latest

ENV CONFIG example.json
ENV PIPELINE_TYPE example_type
ENV SOURCE_TYPE file
ENV SOURCE_NAME labeled_data
ENV DEST_TYPE file
ENV DEST_NAME data.txt

COPY experiment.json ./experiment.json
COPY generator.py ./data_generators/mixing/generator.py
COPY run.py ./data_generators/mixing/run.py

ENV PYTHONPATH ${PYTHONPATH}:

CMD python data_generators/mixing/run.py --config $CONFIG --pipeline-type $PIPELINE_TYPE --source-type $SOURCE_TYPE --source-name $SOURCE_NAME --dest-type $DEST_TYPE --dest-name $DEST_NAME