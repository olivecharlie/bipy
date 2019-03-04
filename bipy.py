import requests
import hmac
import hashlib
import time


class BiPy(object):
	
	BINANCE_BASE_URL = 'https://api.binance.com'
	HEADER_API_KEY = 'X-MBX-APIKEY'
	URI_SIGNED = '{base_url}{endpoint}?{parameters}&signature={signature}'
	URI_UNSIGNED = '{base_url}{endpoint}?{parameters}'
	
	#Unsigned endpoints
	ENDPOINT_TIME = '/api/v1/time'
	ENDPOINT_DEPTH = '/api/v1/depth'
	ENDPOINT_PRICE = '/api/v3/ticker/price'
	
	#Signed endpoints
	ENDPOINT_ALL_ORDERS = '/api/v3/allOrders'
	
	#Status ENUMs
	ORDER_STATUS_NEW = 'NEW'
	ORDER_STATUS_PARTIALLY_FILLED = 'PARTIALLY_FILLED'
	ORDER_STATUS_FILLED = 'FILLED'
	ORDER_STATUS_CANCELED = 'CANCELED'
	#ORDER_STATUS_PENDING_CANCEL = 'PENDING_CANCEL' (currently unused)
	ORDER_STATUS_REJECTED = 'REJECTED'
	ORDER_STATUS_EXPIRED = 'EXPIRED'
		
	def __init__(self, api_key, secret_key):
		self.api_key = api_key
		self.secret_key = secret_key
		
	def __get_headers(self):
		return { self.HEADER_API_KEY : self.api_key }

	def __get_parameters(self, **kwargs):
		parameters = ''
		for k, v in kwargs.items():
			parameters += f'{k}={v}&'
		return parameters[:-1] #to remove the last '&'
		
	def __sign_request(self, parameters):
		return hmac.new(self.secret_key.encode('utf-8'), parameters.encode('utf-8'), hashlib.sha256).hexdigest()
		
	def __get_uri(self, endpoint, signed, **kwargs):
		if signed:
			timestamp = int(time.time() * 1000)
			kwargs['timestamp']=timestamp	
		parameters=self.__get_parameters(**kwargs)
		if signed :
			return self.URI_SIGNED.format(
				base_url=self.BINANCE_BASE_URL, 
				endpoint=endpoint, 
				parameters=parameters,
				signature=self.__sign_request(parameters))
		return self.URI_UNSIGNED.format(
			base_url=self.BINANCE_BASE_URL, 
			endpoint=endpoint, 
			parameters=parameters)

	def ping_time(self):
		'''
		return the current Binance servers time
		A convienient way to test access.
		'''
		uri = self.__get_uri(self.ENDPOINT_TIME, False)
		return requests.get(uri, headers=self.__get_headers()).json()
	
	def get_all_orders(self, **kwargs):
		'''
		get_all_orders:
			symbol
			timestamp
			orderId
			startTime
			endTime
			limit
			recvWindow
		'''	
		uri = self.__get_uri(self.ENDPOINT_ALL_ORDERS, True, **kwargs)
		return requests.get(uri, headers=self.__get_headers()).json()
	
	def get_price(self, **kwargs):
		uri = self.__get_uri(self.ENDPOINT_PRICE, False, **kwargs)
		return requests.get(uri, headers=self.__get_headers()).json()
