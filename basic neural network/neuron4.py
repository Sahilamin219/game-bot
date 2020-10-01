import numpy as np
np.random.seed(0)

X = [[1, 2, 3, 2.5],
     [2.0, 5.0, -1.0, 2.0],
     [-1.5, 2.7, 3.3, -0.8]]

class Dense_Layer(object):
	"""docstring for Layer"""
	def __init__(self, n_inputs, n_neurons):
		self.wgts = 0.1*np.random.randn(n_inputs, n_neurons)
		self.bias = np.zeros((1, n_neurons))
	def forward_pro(self, inputs):
		self.output = np.dot(inputs, self.wgts) + self.bias
		# here we did not took dot of wght*input to save the transpose step


layer1 = Dense_Layer(4,5)
layer2 = Dense_Layer(5,2)

layer1.forward_pro(X)
#print(layer1.output)
layer2.forward_pro(layer1.output)
print(layer2.output)


		

"""
Limitations
Dense layers add an interesting non-linearity property, thus they can model any mathematical function.
However, they are still limited in the sense that for the same input vector we get always the same output vector. 
They can’t detect repetition in time, or produce different answers on the same input.
we can’t do that with dense layers easily 
(unless we increase dimensions which can get quite complicated and has its own limitations). 
That’s where we need recurrent layers.
"""