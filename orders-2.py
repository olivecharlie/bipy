import json
import bipy as bp

with open('_config.json', 'r') as f:
	config = json.load(f)

secret = config['DEFAULT']['SECRET_KEY']
key = config['DEFAULT']['API_KEY']

symbol = 'TRXBTC'

client = bp.BiPy(key, secret)

resp_obj = client.get_all_orders(symbol=symbol)
#print(resp_obj)

for r in resp_obj:
		if r['status'] == 'NEW':
			print('ORDER:')
			for i in r:
				print(f'	{i} : {r[i]}')			
				
'''
watch open orders:
	when they fill:
		place 1% sell for 50% of total amount
		watch price till 0.5% futher rise 
			place stop-loss at original + 0.5%
			every 0.5% rise, lift stop-loss by 0.5%
			...walk it to the moon!
'''
