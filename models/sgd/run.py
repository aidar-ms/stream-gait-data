# Pulls data from the training topic
# Make predictions and pushes predictions to another Kafka topic
import pandas as pd
import numpy as np

from argparse import ArgumentParser
from sklearn.linear_model import SGDClassifier

from core.receiver import Receiver
from core.emitter import Emitter


def get_dfs(record):
    return pd.DataFrame(record["features"]), pd.DataFrame(record["classes"])


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("-st1", "--train-source-type", dest="train_source_type", help="Kafka or file")
    parser.add_argument("-sn1", "--train-source-name", dest="train_source_name", help="Kafka or file")

    parser.add_argument("-st2", "--test-source-type", dest="test_source_type", help="Kafka or file")
    parser.add_argument("-sn2", "--test-source-name", dest="test_source_name", help="Kafka or file")

    parser.add_argument("-pt", "--predictions-dest-type", dest="predictions_dest_type", help="Kafka or file")
    parser.add_argument("-pn", "--predictions-dest-name", dest="predictions_dest_name", help="Kafka or file")

    args = parser.parse_args()

    st1 = args.train_source_type
    sn1 = args.train_source_name

    st2 = args.test_source_type
    sn2 = args.test_source_name
    pt = args.predictions_dest_type
    pn = args.predictions_dest_name

    train_r = Receiver(st1, sn1)
    test_e = Emitter(pt, pn)

    # Initialise the model
    first_run = True
    model =SGDClassifier(
        learning_rate="adaptive",
        eta0=0.01
    )
    i = 0

    for train_record in train_r.stream:
        # Train model
        train_f, train_c = get_dfs(train_record)
        train_f = train_f.reindex(sorted(train_f.columns), axis=1)

        if first_run is True:
            model.partial_fit(train_f, train_c.Surface, classes=train_c.Surface.unique())
            first_run = False
        else:
            model.partial_fit(train_f, train_c.Surface)

        # Make predictions
        test_r = Receiver(st2, sn2)
        for test_record in test_r.stream:
            test_f, test_c = get_dfs(test_record)
            test_f = test_f.reindex(sorted(test_f.columns), axis=1)

            # Write the result
            test_e.send({"iteration": i, "length": len(test_c), "score": model.score(test_f, test_c.Surface)})
        
        test_r.close()
        i += 1
    
    train_r.close()
    test_e.close()
