import bs4 as bs 
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web
import pickle 
import requests

style.use('ggplot')

def get_data_from_user():

	tickers = []
	tickers.append(input("Enter 1st stock:"))
	tickers.append(input("Enter 2nd stock:"))

	with open("tickers.pickle", "wb") as f:
	 	pickle.dump(tickers, f)

	# if reload_sp500:
	# 	tickers = save_sp500_tickers()
	# else:
	# 	with open("tickers.pickle", "rb") as f:
	# 		tickers = pickle.load(f)

	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')

	x = input("From what year do you want the correlation:")
	y = input("From what month do you want the correlation:")
	z = input("From what day do you want the correlation:")
	x = int(x)
	y = int(y)
	z = int(z)

	start = dt.datetime(x,y,z)
	end = dt.datetime(2022,6,17)

	for ticker in tickers:
		print(ticker)
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			df = web.DataReader(ticker, 'yahoo', start, end)
			df.to_csv('stock_dfs/{}.csv'.format(ticker))
		else:
			print('Already have {}'.format(ticker))

get_data_from_user()

def compile_data():
	with open("tickers.pickle", "rb") as f:
	 	tickers = pickle.load(f)

	main_df = pd.DataFrame()

	for count,ticker in enumerate(tickers):
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
		df.set_index('Date', inplace=True)

		df.rename(columns = {'Adj Close': ticker}, inplace=True)
		df.drop(['Open','High','Low','Close','Volume'], 1, inplace=True)

		if main_df.empty:
			main_df = df 
		else:
			main_df = main_df.join(df, how='outer')

		if count % 10 == 0:
			print(count)
	print(main_df.tail())
	main_df.to_csv('tickers_joined_closes.csv')

compile_data()

def visualize_data():
	df = pd.read_csv('tickers_joined_closes.csv')
	df_corr = df.corr()
	print(df_corr.head())

	data = df_corr.values
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)

	heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
	fig.colorbar(heatmap)
	ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
	ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
	ax.invert_yaxis()
	ax.xaxis.tick_top()

	column_labels = df_corr.columns
	row_labels = df_corr.index 

	ax.set_xticklabels(column_labels)
	ax.set_yticklabels(row_labels)
	plt.xticks(rotation=90)
	heatmap.set_clim(-1,1)
	plt.tight_layout()
	plt.show()

visualize_data()

