import unittest
import utility

class UtilityTest (unittest.TestCase):
	
	def test_get_config(self):
		sut = utility.ConfigManager('config.json')
		config = sut.get_config()
		self.assertEqual(config['DEFAULT']['VALUE_ONE'], 'foo')
		self.assertEqual(config['DEFAULT']['SECOND_VALUE'], 'bar')
	
suite = unittest.TestLoader().loadTestsFromTestCase(UtilityTest)
unittest.TextTestRunner(verbosity=2).run(suite)
