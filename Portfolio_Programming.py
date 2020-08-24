"""
Author:		Fengyi
Date Created:	08/08/2020
Description:	The purpose of this program is to pull data from multiple csv textfiles, json
				file, or input data for a investor and analyse his stock and bond performance. 
				Build classes and functions to make necessary calculation. Load data into data-
				base by building new tables and execute insertion, later test if data loading 
				successfully by printing records. Meanwhile provide visualization for stocks'
				values change.
"""

# Import libraries and module
from investment_class import Investor, Stock, Bond, StockTxn
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import sqlite3
import json


# Input investor's information into list
investor_list = []
ID = input("Enter Investor ID: ")				#enter: 001
FName = input("Enter Investor's Firstname: ")   #enter: bob
LName = input("Enter Investor's Lastname: ")	#enter: smith
Address = input("Enter Investor's Address: ")	#enter: colorado blvd 123
City = input("Enter Investor's City: ")			#enter: denver
State = input("Enter Investor's State: ")		#enter: CO
Phone = input("Enter Investor's Phone: ")		#enter: 303-1230000

investor = Investor(ID, FName, LName, Address, City, State, Phone)
investor_list.append(investor)


# Read stock data from text file
stock_file_path = r'C:\Users\Julie\Desktop\Lesson6_Data_Stocks.csv'
def load_data_stock(stock_file_path):
	try:
		stock_file = open(stock_file_path, 'r')
	except FileNotFoundError:
		print ("This file does not exist!")
	else:
		header = stock_file.readline()
		header_split = header.split(',')

		symbol_index = header_split.index('SYMBOL')
		no_shares_index = header_split.index('NO_SHARES')
		purchase_price_index = header_split.index('PURCHASE_PRICE')
		current_value_index = header_split.index('CURRENT_VALUE')
		purchase_date_index = header_split.index('PURCHASE_DATE\n')

		stock_list = []

	for line in stock_file:
		line_split = line.split(',')
		new_stock = Stock(line_split[symbol_index], 
							int(line_split[no_shares_index]),
							float(line_split[purchase_price_index]), 
							float(line_split[current_value_index]),
							line_split[purchase_date_index].strip())
		stock_list.append(new_stock)

	return stock_list
	#print (stock_list)
	stock_file.close()

# Read bond data from text file
bond_file_path = r'C:\Users\Julie\Desktop\Lesson6_Data_Bonds.csv'
def load_data_bond(bond_file_path):
	try: 
		bond_file = open(bond_file_path, 'r')
	except FileNotFoundError:
		print ("This file does not exist!")
	else:
		header = bond_file.readline()
		header_split = header.split(',')

		symbol_index = header_split.index('SYMBOL')
		no_shares_index = header_split.index('NO_SHARES')
		purchase_price_index = header_split.index('PURCHASE_PRICE')
		current_value_index = header_split.index('CURRENT_VALUE')
		purchase_date_index = header_split.index('PURCHASE_DATE')
		coupon_index = header_split.index('Coupon')
		yield_index = header_split.index('Yield\n')

		bond_list = []

		for line in bond_file:
			line_split = line.split(',')
			new_bond = Bond(line_split[symbol_index], 
								int(line_split[no_shares_index]),
								float(line_split[purchase_price_index]), 
								float(line_split[current_value_index]),
								line_split[purchase_date_index], 
								float(line_split[coupon_index]),
								float(line_split[yield_index].strip()))
			bond_list.append(new_bond)
	
	return bond_list
	bond_file.close()

# Load stock & bond data to lists by calling functions
stock_list = load_data_stock(stock_file_path)
bond_list = load_data_bond(bond_file_path)

# Read stock transaction data from JSON file
stockDictionary = {}

json_file_path = r'C:\Users\Julie\Desktop\AllStocks.json'
with open(json_file_path) as json_file:
	data_set = json.load(json_file)

# Use nested for-loop to calculate value for each stock during time
for stock in data_set:
	for new_stock in stock_list:
		if stock['Symbol'] not in stockDictionary:
			newStock = StockTxn(stock['Symbol'], stock['Close'], stock['Date'], new_stock)
			stockDictionary[stock['Symbol']] = newStock
		stockDictionary[stock['Symbol']].value_calc(stock['Symbol'], stock['Close'], 
			datetime.strptime(stock['Date'], '%d-%b-%y'), new_stock)

# Generate graphs for each stock
for stock in stockDictionary:
	symbol = stockDictionary[stock].stock_symbol
	dates = matplotlib.dates.date2num(stockDictionary[stock].stockDateList)
	values = stockDictionary[stock].stockValueList 
	plt.plot_date(dates, values, linestyle='solid', marker='None', label=symbol)

plt.legend()
plt.show()
#plt.savefig('StockPlot.png')

# Define tables for storing data
def create_tables(cursor):
	sql_create_investor_table = """CREATE TABLE IF NOT EXISTS investor (
											investorID text PRIMARY KEY,
											investorName text NOT NULL,
											investorAddress text NOT NULL,
											phone text NOT NULL
											); """

	sql_create_stock_table = """CREATE TABLE IF NOT EXISTS stock (
											stockSymbol text PRIMARY KEY,
											shareNumber integer NOT NULL,
											earningLoss real NOT NULL,
											yearlyEarningLoss text NOT NULL,
											investorID text NOT NULL
											); """

	sql_create_bond_table = """CREATE TABLE IF NOT EXISTS bond (
											bondSymbol text PRIMARY KEY,
											quantity integer NOT NULL,
											earningLoss real NOT NULL, 
											yearlyEarningLoss text NOT NULL,
											coupon real NOT NULL,
											yieldRate real NOT NULL,
											investorID text NOT NULL
											); """

	sql_create_stock_txn_table = """CREATE TABLE IF NOT EXISTS stock_txn (
											stockSymbol text NOT NULL,
											stockDate text NOT NULL,
											stockOpen real NOT NULL,
											stockHigh real NOT NULL,
											stockLow real NOT NULL,
											stockClose real NOT NULL,
											stockVolume integer NOT NULL
											); """

	cursor.execute(sql_create_investor_table)
	cursor.execute(sql_create_stock_table)
	cursor.execute(sql_create_bond_table)
	cursor.execute(sql_create_stock_txn_table)

# Connect to database to create tables
dbPath = r'C:\sqlite\Investment.db'
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

create_tables(cursor)

# Insert data into 4 tables created
def write_data(cursor, investor_list, stock_list, bond_list, data_set):	
	for investor in investor_list:
		sql_insert_investor = "INSERT INTO investor VALUES (" + "'" + investor.investor_id
		sql_insert_investor = sql_insert_investor + "', '" + investor.get_full_name() + "', '"
		sql_insert_investor = sql_insert_investor + investor.get_full_address() + "', '"
		sql_insert_investor = sql_insert_investor + investor.phone + "');"
		cursor.execute(sql_insert_investor)

	for stock in stock_list:
		sql_insert_stock = "INSERT INTO stock VALUES (" + "'" + stock.stock_symbol + "', "
		sql_insert_stock = sql_insert_stock + str(stock.number_of_shares) + ", "
		sql_insert_stock = sql_insert_stock + str(stock.gain_loss_calc()) + ", '"
		sql_insert_stock = sql_insert_stock + str(stock.yearly_pct_calc()) + "', '"
		sql_insert_stock = sql_insert_stock + investor.investor_id + "');"
		cursor.execute(sql_insert_stock)

	for bond in bond_list:
		sql_insert_bond = "INSERT INTO bond VALUES (" + "'" + bond.stock_symbol + "', "
		sql_insert_bond = sql_insert_bond + str(bond.number_of_shares) + ", "
		sql_insert_bond = sql_insert_bond + str(bond.gain_loss_calc()) + ", '"
		sql_insert_bond = sql_insert_bond + str(bond.yearly_pct_calc()) + "', "
		sql_insert_bond = sql_insert_bond + str(bond.coupon) + ", " + str(bond.yield_rate)
		sql_insert_bond = sql_insert_bond + ", '" + investor.investor_id + "');"
		cursor.execute(sql_insert_bond)

	for stock in data_set:
		sql_insert_txn = "INSERT INTO stock_txn VALUES (" + "'" + stock['Symbol'] + "', '"
		sql_insert_txn = sql_insert_txn + str(datetime.strptime(stock['Date'], '%d-%b-%y'))
		sql_insert_txn = sql_insert_txn + "', '" + (stock['Open']) + "', '" + (stock['High'])
		sql_insert_txn = sql_insert_txn + "', '" + (stock['Low']) + "', " + str(stock['Close'])
		sql_insert_txn = sql_insert_txn + ", " + str(stock['Volume']) + ");"
		cursor.execute(sql_insert_txn)

write_data(cursor, investor_list, stock_list, bond_list, data_set)

# Read data from database tables - testing tables created
sql_investor_select = """SELECT rowid, * FROM investor;"""
for record in cursor.execute(sql_investor_select):
	print (record[0], record[1], record[2], record[3])

sql_stock_select = """SELECT rowid, * FROM stock;"""
for record in cursor.execute(sql_stock_select):
	print (record[0], record[1], record[2], record[3], record[4], record[5])

sql_bond_select = """SELECT rowid, * FROM bond;"""
for record in cursor.execute(sql_bond_select):
	print (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7])

sql_stocktxn_select = """SELECT rowid, * FROM stock_txn;"""
for record in cursor.execute(sql_stocktxn_select):
	print (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7])
