input = [[2,4], [3,5], [5,7], [7,10], [9,15]]

def sol(input):
	xpatrat = []
	xy = []
	for i in input:
		xpatrat.append(i[0] * i[0])
		xy.append(i[0] * i[1])
	sumx = sum(i[0] for i in input)
	sumy = sum(i[1] for i in input)
	sumxpatrat = sum(i for i in xpatrat)
	sumxy = sum(i for i in xy)
	
	n = len(input)
	m = (n * sumxy - sumx * sumy) / (n * sumxpatrat - sumx * sumx)
	b = (sumy - m * sumx) / n
	print("y = mx + b este " + "y = " + str(m) + " * x + " + str(b))

	def f(x): return m * x + b
	return f

f = sol(input)

for i in input:
    print("x: " + str(i[0]) + " y: " + str(i[1]) + " f(x): " + str(f(i[0])) + " error [f(x) - y]: " + str((f(i[0]) - i[1])))
