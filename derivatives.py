import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

def initialChoice():
	n = input("Welcome. Please enter your strategy, type options to see available strategies, or type exit to close this program:\n")
	while True:
		choice = str(n)
		if (choice == 'buy call' or choice == 'sell call' or choice == 'buy put' or choice == 'sell put' or choice == 'butterfly spread' or choice == 'bearish vertical spread' or choice == 'top combination' or choice == 'two for one' or choice == 'exit'):
			break
		elif (choice == 'options'):
			n = input("buy call, sell call, buy put, sell put, butterfly spread:\n")
		else:
			n = input("Not a valid input. Please try again or type options to see available strategies:\n")

	return choice

def ownStock():
	price = 56.40
	y = []

	for i in range(80):
		y.append(float(i - price))

	return y

def price(s):
	choice = int(0)
	while True:
		try:
			n1 = input("Enter the " + s + " strike price: ")
			n2 = input("Enter the " + s + " premium: ")
			n1 = float(n1)
			n2 = float(n2)
			break
		except ValueError:
			print("An input was not a number. Please try again.")
	return n1, n2

def call(_type):
	strike, premium = price('call')

	def bought(x):
		val = x
		x = -premium
		if (val > strike): x+= val-strike

		return x

	def sold(x):
		val = x
		x = premium
		if (val > strike): x-= val-strike

		return x

	y = []

	for i in range(80):
		if _type == 'buy':
			y.append(bought(i))
		else:
			y.append(sold(i))

	return y


def put(_type):
	strike, premium = price('put')

	def bought(x):
		val = x
		x = -premium
		if (val < strike): x+= strike-val

		return x

	def sold(x):
		val = x
		x = premium
		if (val < strike): x-= strike-val

		return x

	y = []

	for i in range(80):
		if _type == 'buy':
			y.append(bought(i))
		else:
			y.append(sold(i))

	return y


def total(y, finalY):

	if len(finalY) > 0:
		for i in range(80):
			finalY[i]+= y[i]
	else:
		finalY = y.copy()

	return finalY

def graph(y):
	ticks = [0,40,45,50,55,60,65,70,75]
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	df = pd.DataFrame()
	df['$ per Share'] = y

	#ax.set_xticklabels(ticks)
	maxY = max(y)
	ax.set_xlim([0,80])
	ax.set_ylim([-10,10])
	ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
	ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
	ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')

	#ax.spines['left'].set_position('center')
	ax.spines['bottom'].set_position('center')

	# Show ticks in the left and lower axes only
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')
	ax.xaxis.get_major_ticks()[0].label1.set_visible(False)
	ax.plot(df, linewidth = 1)
	plt.title('Bearish Vertical Spread',fontsize=28)
	plt.xlabel('Share Price', fontsize = 14, labelpad = 2)
	plt.ylabel('$ Value per Share', fontsize = 14)
	plt.show()


def main():
	finalY = []
	y = None
	dType = initialChoice()

	if dType == 'buy call':
		y = call('buy')
		finalY = total(y,finalY)

	if dType == 'sell call':
		y = call('sell')
		finalY = total(y,finalY)

	if dType == 'buy put':
		y = put('buy')
		finalY = total(y,finalY)

	if dType == 'sell put':
		y = put('sell')
		finalY = total(y,finalY)

	if dType == 'butterfly spread':
		y = put('buy')
		finalY = total(y,finalY)
		y = put('sell')
		finalY = total(y,finalY)
		finalY = total(y,finalY)
		y = put('buy')
		finalY = total(y,finalY)

	if dType == 'top combination':
		y = put('sell')
		finalY = total(y,finalY)
		y = call('sell')
		finalY = total(y,finalY)

	if dType == 'two for one':
		y = put('buy')
		finalY = total(y,finalY)
		finalY = total(y,finalY)
		y = ownStock()
		finalY = total(y, finalY)

	if dType == 'bearish vertical spread':
		y = put('sell')
		finalY = total(y,finalY)
		y = put('buy')
		finalY = total(y,finalY)

	print(finalY)
	graph(finalY)


if __name__ == "__main__":
	main()
