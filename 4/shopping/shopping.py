import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and return a tuple (evidence, labels).

    evidence: A list of lists containing feature values.
    labels: A list of integers where 1 indicates Revenue is true, and 0 otherwise.
    """
    df = pd.read_csv(filename)

    df['Month'] = df['Month'].map({
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3,
        'May': 4, 'Jun': 5, 'Jul': 6, 'Aug': 7,
        'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
    })
    df['VisitorType'] = df['VisitorType'].map({'Returning_Visitor': 1, 'New_Visitor': 0})
    df[['Weekend', 'Revenue']] = df[['Weekend', 'Revenue']].astype(int)

    evidence = df.iloc[:, :-1].to_numpy()
    labels = df.iloc[:, -1].to_numpy()

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # return the model KNN with neighbors = 1
    KNN = KNeighborsClassifier(n_neighbors=1)
    KNN.fit(evidence, labels)
    return KNN


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # just calculate the ans 
    positive = 0
    negative = 0
    posiCorrect = 0
    negaCorrect = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            positive += 1
            if predictions[i] == 1:
                posiCorrect += 1
        else:
            negative += 1
            if predictions[i] == 0:
                negaCorrect += 1
    return (posiCorrect / positive, negaCorrect / negative)

# if __name__ == "__main__":
#     main()
    
