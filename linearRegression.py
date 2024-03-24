# Inital imports and setup

import os
import numpy as np

###################
# Helper function #
###################
def load_data(filepath):
    """
    Load in the given csv filepath as a numpy array

    Parameters
    ----------
    filepath (string) : path to csv file

    Returns
    -------
        X, y (np.ndarray, np.ndarray) : (m, num_features), (m,) numpy matrices
    """
    *X, y = np.genfromtxt(
        filepath,
        delimiter=',',
        skip_header=True,
        unpack=True,
    ) # default dtype: float
    X = np.array(X, dtype=float).T # cast features to int type
    return X, y.reshape((-1, 1))

data_filepath = './data/housing_data.csv'
X, y = load_data(data_filepath)

print(X.shape, y.shape) #(90, 3) (90, 1)


def mean_squared_error(y_true, y_pred):
    """
    Calculate mean squared error between y_pred and y_true.

    Parameters
    ----------
    y_true (np.ndarray) : (m, 1) numpy matrix consists of true values
    y_pred (np.ndarray)   : (m, 1) numpy matrix consists of predictions
    
    Returns
    -------
        The mean squared error value.
    """
    #squared error
    se = np.power(y_true - y_pred, 2)

    #mean squared error
    mse = np.mean(se)/2
    return mse


def add_bias_column(X):
    """
    Create a bias column and combine it with X.

    Parameters
    ----------
    X : (m, n) numpy matrix representing a feature matrix
    
    Returns
    -------
        new_X (np.ndarray):
            A (m, n + 1) numpy matrix with the first column consisting of all 1s
    """
    num_of_rows = X.shape[0]
    bias = np.ones((num_of_rows, 1))
    new_X = np.concatenate((bias, X), axis=1)
    return new_X 

def get_bias_and_weight(X, y, include_bias = True):
    """
    Calculate bias and weights that give the best fitting line.

    Parameters
    ----------
    X (np.ndarray) : (m, n) numpy matrix representing feature matrix
    y (np.ndarray) : (m, 1) numpy matrix representing target values
    include_bias (boolean) : Specify whether the model should include a bias term
    
    Returns
    -------
        bias (float):
            If include_bias = True, return the bias constant. Else,
            return 0
        weights (np.ndarray):
            A (n, 1) numpy matrix representing the weight constant(s).
    """
    if include_bias:
        X = add_bias_column(X)
    weights = np.linalg.inv(X.T @ X) @ X.T @ y
    # #####print(weights)
    if include_bias:
        bias_value = weights[0][0]
        w1_to_n_matrix = weights[1:]
    else:
        bias_value = 0
        w1_to_n_matrix = weights
    # #print(bias_value, w1_to_n_matrix)
    return bias_value, w1_to_n_matrix


def get_prediction_linear_regression(X, y, include_bias = True):
    """
    Calculate the best fitting line.

    Parameters
    ----------
    X (np.ndarray) : (m, n) numpy matrix representing feature matrix
    y (np.ndarray) : (m, 1) numpy matrix representing target values
    include_bias (boolean) : Specify whether the model should include a bias term

    Returns
    -------
        y_pred (np.ndarray):
            A (m, 1) numpy matrix representing prediction values.
    """
    
    bias, weights = get_bias_and_weight(X, y, include_bias)

    print("Weights: ", weights)

    y_pred = X @ weights
    
    y_pred = y_pred + bias
    
    return y_pred

import matplotlib.pyplot as plt

area = X[:, 0].reshape((-1, 1))
predicted = get_prediction_linear_regression(area, y)
plt.scatter(area, y)
plt.plot(area, predicted, color = 'r')
plt.xlabel("Size in square meter")
plt.ylabel("Price in SGD")
plt.show()
