# a simple layer of neurons, with 4 inputs.
inputs = [1.0, 2.0, 3.0, 2.5]

weights1 = [0.2, 0.8, -0.5, 1.0]
weights2 = [0.5, -0.91, 0.26, -0.5]
weights3 = [-0.26, -0.27, 0.17, 0.87]

bias1 = 2.0
bias2 = 3.0
bias3 = 0.5

wgt=[]
wgt.append(weights1)
wgt.append(weights2)
wgt.append(weights3)

b=[]
b.append(bias1)
b.append(bias2)
b.append(bias3)

outputs=[0.0]*len(wgt);

for i in range(len(outputs)):
	result=0.0;
	for j in range(len(inputs)):
		result+=inputs[j]*wgt[i][j]
	outputs[i]+=result+b[i]

print(*outputs)