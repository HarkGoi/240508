from urllib.request import urlopen
import json
import datetime

# Generamos la clase que actuará como cliente para utilizar exchangeAPI
class ExchangeClient:
    def __init__(self):
        # la clase ExchangeClient tendrá como atributos los ratios y códigos leidos en el momento de la conexión
        self.rates = self.get_rates()
        self.codes = self.get_codes(self.rates)
    # nos conectamos a la API y obtenemos los ratios
    def get_rates(self):
        api_url = 'https://api.exchangeratesapi.io/latest'
        # solicitamos información a la URL
        response = urlopen(api_url)
        # cargamos los datos en formato JSON
        rates = json.loads(response.read())
        # devolvemos el diccionario correspondiente
        return rates['rates']
    def get_codes(self,rates):
        return list(rates.keys())
    def change(self,rates,quantity,original,to='EUR'):
        return float(quantity) / float(rates[original])
'''
    def convert(cantidad, de='EUR', a='USD'): 
        rates = get_rates()
        return rates['USD'] * cantidad
'''

if __name__ == '__main__':
    # obtenemos los ratios y códigos
    exClient = ExchangeClient()

    # abrimos el fichero de ahorros y vamos convirtiendo los datos
    with open('savings.txt','r') as file:
        total = 0
        lineas = file.readlines()
        i=0
        for linea in lineas:
            i+=1
            # hacemos la lectura desde savings (csv) manualmente (no merece la pena utilizar la librería) para un
            # ejemplo tan pequeño
            [code,quantity] = linea.strip().split(',') # lista = [moneda,cantidad]
            if code in exClient.codes:
                total += exClient.change(exClient.rates,quantity,code)
            else:
                print('Código incorrecto en la linea {}'.format(i))

    # escribimos el resultado en el fichero de evolución
    with open('evolution.txt','a') as file:
        # generamos el objeto daytime actual para extraer los atributos que nos interesan
        dt = datetime.datetime.now()
        file.writelines('{}, {}\n'.format(dt.strftime('%c'),total))