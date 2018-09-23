This python notebook file contains an experiment investigating the error
score and error standard deviation score dependency of a single hidden layer
neural network with 6 neurons in the hidden layer on the number of epochs in iteration procedure.

The Iris dataset (http://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html)
is used for this experiment. The data set must be divided into three classes.
Neural network is built with Keras library. Dataset is split into parts for cross validation.
The results can be seen in the plot graphs.

In the picture error.png it can be seen that the more iterations are made the less the error score is.
In the picture error_std.png it can be seen that error standard deviation dependency on the number of iterations has
a decreasing trend.
