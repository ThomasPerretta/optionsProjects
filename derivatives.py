import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def current():
	n = input("What position would you like to open? \n" )
	while True:
		choice = str(n)
		if (choice == 'long call' or 
			choice == 'short call' or 
			choice == 'long put' or 
			choice == 'short put' or 
			choice == 'long stock' or 
			choice == 'short stock' or
			choice == 'exit'):
			break
		elif (choice == 'options'):
			n = input("long stock, short stock \nlong call, short call \nlong put, short put \nlend, borrow \noptions, exit:\n")
		else:
			n = input("Not a valid input. Please try again or type options to see available strategies:\n")

	return choice.replace(' ', '')

def price(asset):
	val = 0.0
	while True:
		try:
			val = float(input("Enter " + asset + " price:"))
			break			
		except ValueError:
			print("Input not valid. Please try again.")

	return val

def longstock(expr):
	v = price('stock')
	s = Symbol('s')
	expr+= s - v
	return expr

def shortstock(expr):
	v = price('stock')
	s = Symbol('s')
	expr+= v - s
	return expr

def longcall(expr):
	k = price('strike')
	c = price('call')
	s = Symbol('s')
	expr+= Piecewise((0, s-k < 0), (s-k, True)) - c
	return expr

def shortcall(expr):

	k = price('strike')
	c = price('call')
	s = Symbol('s')
	expr+= c - Piecewise((0, s-k < 0), (s-k, True)) 
	return expr

def longput(expr):

	k = price('strike')
	p = price('put')
	s = Symbol('s')
	expr+= Piecewise((0, k-s < 0), (k-s, True)) - p
	return expr

def shortput(expr):

	k = price('strike')
	p = price('put')
	s = Symbol('s')
	expr+= p - Piecewise((0, k-s < 0), (k-s, True)) 
	return expr

def evaluate(expr):
	s = Symbol('s')
	fd = diff(expr)
	breakEven = solveset(expr,s, domain=S.Reals)
	criticalPoints = solveset(fd,s, domain=S.Reals)

	bEs = set()
	cPs = set()
	for arg in breakEven.args:
		bEs.add(arg)


	for arg in criticalPoints.args:
		cPs.add(arg)

	finalBEs = [round(x,2) for x in bEs if (isinstance(x, Float))] #sympy.core.numbers.Float type
	finalCPs = [round(x,2) for x in cPs if (isinstance(x, Float))]

	print('Break even point(s) at: ' + str(finalBEs))
	print('Inflection point(s) at: ' + str(finalCPs))
	plotRange = finalBEs+finalCPs
	return plotRange, finalBEs, finalCPs, 

def plot(expr, plotRange, breakEvens, criticalPoints):
	
	#Generate plots to be plotted
	s = Symbol('s')
	x = []
	y = []
	minR = min(plotRange)
	maxR = max(plotRange)

	
	for i in np.arange(0.75 * minR, 1.25* maxR,0.1):

		if breakEvens and breakEvens[0] < i:
			x.append(breakEvens[0])
			y.append(float(expr.subs(s, breakEvens[0])))
			breakEvens.pop(0)

		if criticalPoints and criticalPoints[0] < i:
			x.append(criticalPoints[0])
			y.append(float(expr.subs(s, criticalPoints[0])))
			criticalPoints.pop(0)

		x.append(i)
		y.append(float(expr.subs(s, i)))

	df = pd.DataFrame()
	df['Stock Price'] = x
	df['$ per Share'] = y
	df = df.set_index('Stock Price')
	
	sns.set(style="darkgrid", palette="muted", color_codes=True)
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')

	#ax.spines['bottom'].set_position('center')

	plt.xlim(x[0], x[-1])
	plt.title('Payoff Diagram',fontsize=18, pad = 16)
	plt.xlabel('Stock Price', fontsize = 14, labelpad = 8)
	plt.ylabel('$ Value per Share', fontsize = 14, labelpad = 8)


	plt.plot([x[0],x[-1]], [0,0], c= 'lightgrey') #Horizontal Line

	plt.plot(df) #Main line

	for i in plotRange: #Points of inflection / breakeven
		plt.plot(i, float(expr.subs(s, i)), 'ro', c = 'orange')
		

	plt.show()
	

def main():
	dType = current()
	expr = 0

	while dType != 'exit':
		expr = globals()[dType](expr)
		dType = current()

	if expr != 0:
		plotRange, breakEvens, criticalPoints = evaluate(expr)
		plot(expr, plotRange, breakEvens, criticalPoints)


if __name__ == "__main__":
	main()
