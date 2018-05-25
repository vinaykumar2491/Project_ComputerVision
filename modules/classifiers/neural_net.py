import numpy as np
import matplotlib.pyplot as plt


class TwoLayerNet(object):
    """
    A two-layer fully connected neural network.
    The network:
            dim(input) = N
            dim(hidden) = H
            dim(output) = C

            loss-function : Softmax
            Regularization : L2
            Nonlinearilty : ReLU

    The network has the following architecture:
    Input -> FC-layer_1 -> ReLU -> FC-layer_2 -> softmax

    The output of "FC_layer_2" are the scores for each class in C

    """

    def __init__(self, input_size, hidden_size, output_size, std=1e-4):
        """
        Initializes the model.
        Weights(W1, W2) are initialized to small random values.
        Biases(b1, b2) are initialized to ZERO

        All weights and biases are stored in a 'dict' self.params with following keys:
                W1 : First-layer weights : shape = (D,H)
                b1 : First-layer biases  : shape = (H,)
                W2 : Second-layer weights: shape = (H,C)
                b2 : Second-layer biases : shape = (C,)

        Inputs:
        - input_size  : The dimension D of the input data
        - hidden_size : The number of neurons H in the hidden layer
        - output_size : The number of classes

        """
        self.params = {}
        self.params['W1'] = std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)

    def loss(self, X, y=None, reg=0.0):
        """
        Computes the loss and gradients for a two-layer fully connected neural network

        Inputs:
        - X : Input data of shape (N,D). Each X[i] is a training sample
        - y : Vector of training labels. y[i] is the label for X[i].
                        0 <= y[i] <= C
                  This is optional. If y is NOTot given as an input then we just return the scores.
                  If y is given as an input then we return both 'scores' and 'gradients'
        - reg : Regularization strength

        Returns:
                Case-1 : If y is None the just return the scores matrix of shape (N, C)
                                        where scores[i,c] is the score of X[i] for tha label c
                Case-2 : If y is NOT None, returns a tuple of (loss, grads)
        - loss : Loss(data loss and regularization loss)
        - grads : Dictionary mapping parameter names to gradients of those parameters wrt the loss function;
                                has the same keys as self.params (i.e. W1, b1, W2, b2)

        """

        N, D = X.shape
        W1 = self.params['W1']
        b1 = self.params['b1']
        W2 = self.params['W2']
        b2 = self.params['b2']

        loss = None        # shape : integer
        scores = None      # shape : (N, C)
        grads = {}

        ################-------------- FORWARD pass -------------------#####################
        ########    X -> (W1, b1) -> ReLU -> (W2, b2) -> scores/labels/FC   ################

        # perform the Forward pass computing the class scores for the input
        # Store the scores in an array of shape (N, C)

        scores_layer0 = X.dot(W1) + b1                   # layer-1 scores
        scores_h1 = np.maximum(0, scores_layer0)         # ReLU nonlinearity
        scores = scores_h1.dot(W2) + b2                 # last layer scores : layer-2 scores

        # check if the targets (i.e. y) are given or not
        # if y == None:
        #     return scores       # if the targets are not given then just return the scores

        # If the targets are given the compute the loass and calculate the gradients
        # compute the SOFTMAX loss

        scores -= np.transpose([np.max(scores, axis=1)])    # normalization trick to prevent exponentiation boom
        scores_exp = np.exp(scores)     # exponentiation
        scores_exp_norm = scores_exp / np.sum(scores_exp, axis=1)[:, None]   # L_i : normalization

        #  softmax loss : L = (1/N) * sum(L_i) + (lambda * R^2)
        loss = np.sum(-1*np.log(scores_exp_norm[np.arange(N), y]))
        loss /= N
        loss += reg * (np.sum(W1*W1) + np.sum(W2*W2))       # L2 regularization


        ####################-------------- BACKWARD pass -------------------################################
        ########    layer-2 gradients : grads[layer-2] <- ((W2, b2) <- scores)                  ############
        ########    layer-1 gradients : grads[layer-1] <- ((W1, b1) <- ReLU <- (W2 <- scores))  ############

        # compute the gradients:
        # dL_i/dW = -X_i + sum(X_j * L_i)          (NOTE: symbols interpretable only for one layer; for multiple layers interpret accordingly)
        # dL_i/db = -1 + sum(L_i)
        
        # layer-2 gradients
        dSoft = scores_exp_norm.copy()
        dSoft[np.arange(N), y] -= 1
        dSoft /= N      # dL/dW = (1/N)*sum(dL_i/dW)
        grads['W2'] = scores_h1.T.dot(dSoft) + 2 * reg * W2     # adding the gradient for regularization term
        grads['b2'] = np.sum(dSoft, axis=0)

        # layer-1 gradients
        mask_ReLU = scores_h1 > 0
        dh1 = dSoft.dot(W2.T)
        dh1_ReLU = mask_ReLU * dh1
        grads['W1'] = X.T.dot(dh1_ReLU) + 2 * reg * W1
        grads['b1'] = np.sum(dh1_ReLU, axis=0)

        return loss, grads

    #########################################################################################
