import bipy as bp
import utility as util

class Trader (object):
		
	def __init__(self, config_manager):
		self.config_manager = config_manager
		
	def connect(self):
		#logon to binance
		config = self.config_manager.get_config()
		secret = config
		key = config
		print(f'{key} - {secret}')	
		#create client
		#self.client = bp.BiPy(key, secret)
		return secret
	
	def load_watch_trade():
		print('Connecting and retrieving watch trades...')
