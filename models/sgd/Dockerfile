FROM aidarms/stream-gait:latest

ENV PYTHONPATH ${PYTHONPATH}:.

ENV TRAIN_SOURCE_TYPE file
ENV TRAIN_SOURCE_NAME train_data

ENV TEST_SOURCE_TYPE file
ENV TEST_SOURCE_NAME test_data
ENV PREDICTIONS_DEST_TYPE file
ENV PREDICTIONS_DEST_NAME test_data

COPY run.py ./models/sgd/run.py

CMD python models/sgd/run.py \
    --train-source-type ${TRAIN_SOURCE_TYPE} --train-source-name ${TRAIN_SOURCE_NAME} \
    --test-source-type ${TEST_SOURCE_TYPE} --test-source-name ${TEST_SOURCE_NAME} \
    --predictions-dest-type ${PREDICTIONS_DEST_TYPE} --predictions-dest-name ${PREDICTIONS_DEST_NAME}