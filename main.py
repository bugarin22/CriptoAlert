import requests
import keys
import pandas as pd
from time import sleep
import os
import datetime

def get_crypto_rates(base_currency='USD', assets='SHIB'):
        url = 'https://api.nomics.com/v1/currencies/ticker'

        payload = {'key': keys.NOMICS_API_KEY, 'convert': base_currency, 'ids': assets, 'interval': '1d'}
        response = requests.get(url, params=payload)
        data = response.json()

        crypto_currency, crypto_price, crypto_timestamp = [], [], []

        for asset in data:
                crypto_currency.append(asset['currency'])
                crypto_price.append(asset['price'])
                crypto_timestamp.append(asset['price_timestamp'])

        raw_data = {
                'assets' : crypto_currency,
                'rates' : crypto_price,
                'timestamp' : crypto_timestamp
                }

        df = pd.DataFrame(raw_data)
      
        return df

def set_alert(dataframe, asset, alert_high_price):
	crypto_value = float(dataframe[dataframe['assets'] == asset]['rates'].item())
	
	details = f'{asset}: {"%.8f" % crypto_value}, ValorMinimo: {"%.8f" % alert_high_price}'
	
	os.environ['GeeksForGeeks'] = details
	
	now = datetime.datetime.now()
	hour = '{:02d}'.format(now.hour)
	global loop
	
	if crypto_value <= alert_high_price:
		print(details + ' << VALOR MINIMO ALCANZADO!!')
		os.system('/home/pi/tg/bin/telegram-cli -k /home/pi/tg/tg-server.pub -W -e "msg Chavo ALERTA VALOR MINIMO ALCANZADO!! $GeeksForGeeks"')
		sleep(5)
		#print("GeeksForGeeks:", os.environ['GeeksForGeeks'])
		os.system('/home/pi/tg/bin/telegram-cli -k /home/pi/tg/tg-server.pub -W -e "msg Nene_Buga ALERTA VALOR MINIMO ALCANZADO!! $GeeksForGeeks"')
		
	elif ((hour!=0 or hour!=1 or hour!=2 or hour!=3 or hour!=4 or hour!=5 or hour!=6 or hour!=7) and (loop >= 60)):
		loop=0
		print(hour)
		print(details)
		os.system('/home/pi/tg/bin/telegram-cli -k /home/pi/tg/tg-server.pub -W -e "msg Chavo ACTUALIZACION Precio SHIBA cada hora!! $GeeksForGeeks"')
		sleep(5)
		#print("GeeksForGeeks:", os.environ['GeeksForGeeks'])
		os.system('/home/pi/tg/bin/telegram-cli -k /home/pi/tg/tg-server.pub -W -e "msg Nene_Buga ACTUALIZACION Precio SHIBA cada hora!! $GeeksForGeeks"')
	
	else:
		print(details)
		
		
#Alert While Loop
loop = 1
while True:
	print(f'------------------------ ({loop}) ------------------------')
	
	try:
		df= get_crypto_rates()
		
		set_alert(df, 'SHIB', 0.000060)
		
	except Exception as e:
		print('Couldn\'t retrive the data ... Trying again.')
	
	loop +=1
	sleep(60)
