"""
Author:		Fengyi(Julie)
Date Created:	08/23/2020
Description:	This module is to create classes to support main code in Portfolio_
				Programming.py.
"""

from datetime import datetime

class Investor:
	"""A simple attempt to represent an investor."""
	def __init__(self, investor_id, firstname, lastname, address, city, state, phone):
		"""Initialize attributes to describe an investor."""
		self.investor_id = investor_id
		self.firstname = firstname
		self.lastname = lastname
		self.address = address
		self.city = city
		self.state = state
		self.phone = phone

	def get_full_name(self):
		"""Return a full name."""
		full_name = f"{self.firstname} {self.lastname}"
		return full_name.title()

	def get_full_address(self):
		"""Return combined address with case sensitive."""
		full_address = f"{self.address.title()}, {self.city.title()}, "
		full_address = full_address + f"{self.state.upper()}"  # get upper case
		return full_address

class Stock:
	"""Represent aspects to model a stock for investor."""
	def __init__(self, stock_symbol, number_of_shares, purchase_price, current_value,
		purchase_date):
		"""Initialize attributes to describe a stock."""
		self.stock_symbol = stock_symbol
		self.number_of_shares = number_of_shares
		self.purchase_price = purchase_price
		self.current_value = current_value
		self.purchase_date = purchase_date

	def gain_loss_calc(self):
		"""Calculate total gain or loss for stock."""
		total_cost = self.purchase_price*self.number_of_shares
		total_value = self.current_value*self.number_of_shares
		self.total_gain_loss = round((total_value - total_cost), 2)
		return self.total_gain_loss

	def yearly_pct_calc(self):
		"""Calculate yearly earning loss percentage for stock."""
		yield_loss_share = self.current_value - self.purchase_price
		yield_loss_pct = yield_loss_share/self.purchase_price
		current_date = datetime.today()
		purchase_date = datetime.strptime(self.purchase_date, '%m/%d/%Y')
		day_diff = (current_date - purchase_date).days
		year_diff = round((day_diff/365), 2)
		self.yearly_earning_loss = "{:.2%}".format(yield_loss_pct/year_diff)
		return self.yearly_earning_loss

class Bond(Stock):
	"""Represent aspects of a bond, inheriting to Stock."""
	def __init__(self, stock_symbol, number_of_shares, purchase_price, current_value,
		purchase_date, coupon, yield_rate):
		"""Initialize attributes of the parent class Stock."""
		super().__init__(stock_symbol, number_of_shares, purchase_price, current_value, 
			purchase_date)
		self.coupon = coupon
		self.yield_rate = yield_rate

class StockTxn:
	def __init__(self, stock_symbol, close_price, date, stock):
		"""Initialize attributes to describe stock transcation."""
		self.stock_symbol = stock_symbol
		self.close_price = close_price
		self.date = date
		self.stock = stock
		self.stockValueList = []
		self.stockDateList = []
		self.stockVolumeList = []

	def value_calc(self, stock_symbol, close_price, date, stock):
		"""Calculate for stockValueList and stockDateList."""
		if stock_symbol == stock.stock_symbol:
			value = round((close_price * stock.number_of_shares), 2)
			self.stockValueList.append(value)
			self.stockDateList.append(date)


