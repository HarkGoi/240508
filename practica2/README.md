Se han tomado las siguientes decisiones (también están comentadas en el .py):
- Se han definido dos atributos para la clase ExchangeClient, rates (contiene el diccionario con los ratios) y codes
  (contiene los códigos del diccionario). Ambos se obtienen al generar el objeto y se pueden actualizar en caso de
  necesitarlo llamando a las funciones get_rates y get_codes.
- La lectura de el fichero savings.txt se ha hecho a mano, ya que importar la librería para un programa tan pequeño una
  vez implementada la lectura me parecía un error.
- Se ha tomado la decisión de que en caso de que haya un error en un código (por ejemplo poner YEN en lugar de JPY) se
  informe de la linea en la que está el error y se continúe procesando el resto.
- Se ha realizado la escritura de la fecha y hora de cada suma utilizando la clase datetime.