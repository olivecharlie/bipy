import unittest
from unittest import mock
from utility import ConfigManager
import trader


class TraderTests(unittest.TestCase):
	
	def test_connect(self):
		with mock.patch('utility.ConfigManager') as MockConfig:
			MockConfig.return_value.get_config.return_value = '{ "DEFAULT" : {"VALUE_ONE" : "foo", "SECOND_VALUE" : "bar" }}'
			sut = trader.Trader(MockConfig)
			sut.g
			MockConfig.asset_called_once
			print(f'result {sut.connect()}')
				
suite = unittest.TestLoader().loadTestsFromTestCase(TraderTests)
unittest.TextTestRunner(verbosity=2).run(suite)
