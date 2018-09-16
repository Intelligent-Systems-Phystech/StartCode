This python notebook file contains an experiment investigating the accuracy
score and standard deviation score dependency of a single hidden layer
neural network on the number of neurons in the hidden layer.

The Iris dataset (http://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html)
is used for this experiment. The data set must be divided into three classes.
Neural network is built with Keras library. Dataset is split into parts for cross validation.
The results can be seen in the plot graphs.

In the picture accuracy.png it can be seen that adding neurons to the hidden layer
increases the accuracy score to a certain value and then it fluctuates around this value (saturation level).
In the picture std.png it can be seen that adding neurons to the hidden layer
decreases the standard deviation score to a certain value and then it fluctuates around this value (saturation level).
Both the accuracy and standard deviation scores reach their saturation levels at the same number of
neurons in the hidden layer.
