from urllib.request import urlopen
import json
import datetime

# Generamos la clase que actuará como cliente para utilizar exchangeAPI
class ExchangeClient:
    def_ini
    # nos conectamos a la API y obtenemos los ratios
    def get_rates(self):
        api_url = 'https://api.exchangeratesapi.io/latest'
        # solicitamos información a la URL
        response = urlopen(api_url)
        # cargamos los datos en formato JSON
        rates = json.loads(response.read())
        # devolvemos el diccionario correspondiente
        return rates['rates']
    def codes(self,rates):
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
    rates = exClient.get_rates()
    codes = exClient.codes(rates)

    # abrimos el fichero de ahorros y vamos convirtiendo los datos
    with open('savings.txt','r') as file:
        total = 0
        lineas = file.readlines()
        i=0
        for linea in lineas:
            i+=1
            [code,quantity] = linea.strip().split(',') # lista = [moneda,cantidad]
            if code in codes:
                total += exClient.change(rates,quantity,code)
            else:
                print('Código incorrecto en la linea {}'.format(i))

    # escribimos el resultado en el fichero de evolución
    with open('evolution.txt','a') as file:
        file.writelines('{}, {}'.format(datetime.datetime.now(),total))