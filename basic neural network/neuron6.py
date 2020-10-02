# file=open('create.txt')
# try:
    
# finally:
#     file.close()
#our filel should be in csv format
import numpy as np
def sigmoid(z):
    s=1/1+np.exp(-z)
    return s
class neuralnetwork:
    def __init__(self,x,y):
        self.input=x
        self.input=y
        self.weigths1=1
        self.weights2=2
    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))
        