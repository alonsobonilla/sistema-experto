import csv

reglas = dict()
sintomas_usuario = dict()
leyenda = dict()

"""
Obtengo las reglas del csv. 
Permite obtener todos los tipos de anemia y obtener los sintomas que son obligatorios y opcionales para cada tipo de anemia
"""
with open('reglas.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    #Obtengo los tipos de anemia accediento a la primera fila del csv
    for tipo in spamreader.__next__():
        if tipo != '': 
            reglas[tipo] = dict()
            leyenda[tipo] = set()

    #Obtengo las reglas para cada tipo de anemia
    for row in spamreader:
        for k ,v in enumerate(reglas):
            k += 1
            #Si la celda es x, significa que el sintoma es obligatorio para el tipo de anemia
            if row[k] == 'x':
                reglas[v][row[0]] = True
            
                """
                Si la celda es diferente a vacia, osea es una letra de un grupo de sintomas opcionales, (y,z,u,f,etc - ver excel) significa que el sintoma es opcional para el tipo de anemia
                """
            elif row[k] != '':
                #Agrego la letra a la leyenda del tipo de anemia. Agrupo los sintomas opcionales con una letra (ver excel)
                leyenda[v].add(row[k])

                #Agrego al diccionario de reglas de un tipo de anemia la letra que abarca a los sintoams opcionales
                try:
                    reglas[v][row[k]][row[0]] = True
                except KeyError:
                    reglas[v][row[k]] = {row[0]: True}

        #Agrego los sintomas que existen al diccionario de sintomas del usuario            
        sintomas_usuario[row[0]] = False

"""
Valida los sintomas del usuario con las reglas del tipo de anemia que se le pase.
"""
def validar_sintomas(tipo_anemia):
    min_sintomas_opcionales = len(leyenda[tipo_anemia]) #Total de sintomas opcionales que tiene el tipo de anemia
    contador = 0 #Contador de sintomas opcionales que tiene el usuario

    """
        Si el usuario tiene todos los sintomas obligatorios (contador = 0 y min_sintomas_opcionales = 0), entonces validamos que tenga los sintomas del tipo de anemia que se le pasa como parámetro.
    """
    if contador == min_sintomas_opcionales and sintomas_usuario == reglas[tipo_anemia]:
        return True

    reglas_copia = reglas[tipo_anemia].copy() #Copia de las reglas del tipo de anemia

    sintomas_usuario_copia_validacion_final = dict() #Diccionario que contendrá los sintomas del usuario que son obligatorios para el tipo de anemia que se le pasa como parámetro

    """
        Llenamos el diccionario sintomas_usuario_copia_validacion_final con los sintomas del usuario que son obligatorios para el tipo de anemia que se le pasa como parámetro.
    """
    for k, v in sintomas_usuario.items():
        if k in reglas_copia:
            sintomas_usuario_copia_validacion_final[k] = v
    
    #Recorremos las letras que abarcan a los sintomas opcionales del tipo de anemia (ver excel)
    for k in leyenda[tipo_anemia]:
        sintomas = reglas_copia.pop(k) #Obtenemos los sintomas opcionales de la letra que estamos recorriendo

        #Recorremos los sintomas opcionales
        for j, _ in sintomas.items():
            valor = sintomas_usuario[j] #Obtenemos el valor del sintoma del usuario

            """
            Si el usuario tiene al menos un sintoma opcional, entonces aumentamos el contador y ya no recorremos los demás sintomas opcionales y pasamos al otro grupo de sintomas opcionales si es que hubiera
            """
            if valor: 
                contador += 1
                break 
    """
    Si el contador es igual a la cantidad minima de sintomas opcionales (total de grupo de letras) que tiene el tipo de anemia y si los sintomas del usuario que son obligatorios son iguales a las reglas para el tipo de anemia, entonces el usuario tiene el tipo de anemia que se le pasa como parámetro
    """
    
    if contador == min_sintomas_opcionales and reglas_copia == sintomas_usuario_copia_validacion_final:
        return True
    return False
    

if __name__ == '__main__':
    for k, v in sintomas_usuario.items():
        sintomas_usuario[k] = True if input("¿Tiene " + k + "? (s/n)") == 's' else False

    if validar_sintomas('Hemolítica'):
        print('Tiene anemia hemolítica')
    elif validar_sintomas('Aplásica'):
        print('Tiene anemia aplásica')
    elif validar_sintomas('Por deficiencia de hierro'):
        print('Tiene anemia por deficiencia de hierro')
    elif validar_sintomas('Por deficiencia de vitaminas'):
        print('Tiene anemia por deficiencia de vitaminas')
    else:
        print('No cumple con las reglas de los tipos de anemia')
