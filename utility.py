import json

class ConfigManager (object):
	
		def __init__(self, file_path):
			self.file_path = file_path
			
		def get_config(self):
			with open(self.file_path, 'r') as f:
				config = json.load(f)
			return config
