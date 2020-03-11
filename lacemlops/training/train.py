# import os
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
import lightgbm


def split_data(data_df):
    """Split a dataframe into training and validation datasets"""
    features = data_df.drop(['target', 'id'], axis=1)
    labels = np.array(data_df['target'])
    features_train, features_valid, labels_train, labels_valid = train_test_split(features, labels, test_size=0.2, random_state=0)  # noqa: E501
    train_data = lightgbm.Dataset(features_train, label=labels_train)
    valid_data = lightgbm.Dataset(features_valid, label=labels_valid,
                                  free_raw_data=False)
    return (train_data, valid_data)


def train_model(data, parameters):
    """Train a model with the given datasets and parameters"""
    # The data returned in split_data is an array.
    # Access train_data with data[0] and valid_data with data[1]
    train_data = data[0]
    valid_data = data[1]
    model = lightgbm.train(parameters,
                           train_data,
                           valid_sets=valid_data,
                           num_boost_round=500,
                           early_stopping_rounds=20)
    return model


def get_model_metrics(model, data):
    """Construct a dictionary of metrics for the model"""
    validation_data = data[1]
    predictions = model.predict(validation_data.data)
    fpr, tpr, thresholds = metrics.roc_curve(validation_data.label, predictions)  # noqa: E501
    model_metrics = {"auc": (metrics.auc(fpr, tpr))}
    return model_metrics


def main():
    """This method invokes the training functions for development purposes"""
    # Read data from a file
    data_df = pd.read_csv('porto_seguro_safe_driver_prediction_train.csv')
    # Hard code the parameters for training the model
    parameters = {
        'learning_rate': 0.02,
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'metric': 'auc',
        'sub_feature': 0.7,
        'num_leaves': 60,
        'min_data': 100,
        'min_hessian': 1,
        'verbose': 2
    }
    # Call the functions defined in this file
    data = split_data(data_df)
    model = train_model(data, parameters)
    # Print the resulting metrics for the model
    model_metrics = get_model_metrics(model, data)
    print(model_metrics["auc"])


if __name__ == '__main__':
    main()
