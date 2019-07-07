# https://docs.python.org/2/library/unittest.html
import unittest
import bipy


class BiPyTests(unittest.TestCase):
    RESULT_PARAMETER_LIST = 'symbol=TRXBTC&timestamp=1550964774431'
    RESULT_SIGNED_PARAMETER_LIST = 'cdc1600741ccb157765fc3e8c2fb35a04ef1fed472744d074bff7b12888aa4a0'
    REGEX_GET_URI_SIGNED = 'https:\/\/api\.binance\.com\/api\/v3\/allOrders\?symbol=TRXBTC&timestamp=\d{13}&signature=[a-f0-9]{64}'
    RESULT_GET_URI_UNSIGNED = 'https://api.binance.com/api/v1/depth?symbol=TRXBTC&limit=20'
    RESULT_GET_URI_UNSIGNED_NO_PARAMETERS = 'https://api.binance.com/api/v3/ticker/price?'
    REGEX_GET_ALL_ORDERS = "https:\/\/api\.binance\.com\/api\/v3\/allOrders\?symbol=TRXBTC&timestamp=\d{13}&signature=[a-f0-9]{64}"
    REGEX_TIMESTAMP = "\d{13}"

    def test__get_headers(self):
        sut = bipy.BiPy('key', 'secret')
        self.assertEqual(sut._BiPy__get_headers(), {'X-MBX-APIKEY': 'key'})

    def test__get_parameters(self):
        sut = bipy.BiPy('key', 'secret')
        self.assertEqual(sut._BiPy__get_parameters(symbol='TRXBTC', timestamp=1550964774431),
                         self.RESULT_PARAMETER_LIST)

    def test__sign_request(self):
        sut = bipy.BiPy('key', 'secret')
        self.assertEqual(sut._BiPy__sign_request(self.RESULT_PARAMETER_LIST), self.RESULT_SIGNED_PARAMETER_LIST)

    def test__get_uri_when_signed(self):
        sut = bipy.BiPy('key', 'secret')
        self.assertRegexpMatches(sut._BiPy__get_uri(bipy.BiPy.ENDPOINT_ALL_ORDERS, True, symbol='TRXBTC'),
                                 self.REGEX_GET_URI_SIGNED)

    def test__get_uri_when_unsigned(self):
        sut = bipy.BiPy('key', 'secret')
        self.assertEqual(sut._BiPy__get_uri(bipy.BiPy.ENDPOINT_DEPTH, False, symbol='TRXBTC', limit=20),
                         self.RESULT_GET_URI_UNSIGNED)

    def test__get_uri_when_unsigned_no_parameters(self):
        sut = bipy.BiPy('key', 'secret')
        self.assertEqual(sut._BiPy__get_uri(bipy.BiPy.ENDPOINT_PRICE, False),
                         self.RESULT_GET_URI_UNSIGNED_NO_PARAMETERS)


suite = unittest.TestLoader().loadTestsFromTestCase(BiPyTests)
unittest.TextTestRunner(verbosity=2).run(suite)
