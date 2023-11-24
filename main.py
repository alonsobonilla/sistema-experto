import csv

reglas = dict()
sintomas_usuario = dict()
leyenda = dict()

#Obtengo las reglas del csv
with open('reglas.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    for tipo in spamreader.__next__():
        if tipo != '': 
            reglas[tipo] = dict()
            leyenda[tipo] = set()

    #Obtengo las reglas para cada tipo de anemia
    for row in spamreader:
        for k ,v in enumerate(reglas):
            k += 1
            if row[k] != '' and row[k] == 'x':
                reglas[v][row[0]] = True
            elif row[k] != '':
                leyenda[v].add(row[k])
                try:
                    reglas[v][row[k]][row[0]] = True
                except KeyError:
                    reglas[v][row[k]] = {row[0]: True}
                    
        sintomas_usuario[row[0]] = False

#Pregunto al usuario por los sintomas
def validar_cualquier_opcion(tipo_anemia):
    min_reglas = len(leyenda[tipo_anemia])
    contador = 0

    if contador == min_reglas and sintomas_usuario == reglas[tipo_anemia]:
        return True

    reglas_copia = reglas[tipo_anemia].copy()

    sintomas_usuario_copia_validacion_final = dict()
    sintomas_usuario_copia = sintomas_usuario.copy()

    for k, v in sintomas_usuario.items():
        if k in reglas_copia:
            sintomas_usuario_copia_validacion_final[k] = v
    
    for k in leyenda[tipo_anemia]:
        sintomas = reglas_copia.pop(k)

        for j, _ in sintomas.items():
            valor = sintomas_usuario_copia.pop(j)
            if valor:
                contador += 1
                break

    if contador == min_reglas and reglas_copia == sintomas_usuario_copia_validacion_final:
        return True
    

if __name__ == '__main__':
    for k, v in sintomas_usuario.items():
        sintomas_usuario[k] = True if input("¿Tiene " + k + "? (s/n)") == 's' else False

    if validar_cualquier_opcion('Hemolítica'):
        print('Tiene anemia hemolítica')
    elif validar_cualquier_opcion('Aplásica'):
        print('Tiene anemia aplástica')
    elif validar_cualquier_opcion('Por deficiencia de hierro'):
        print('Tiene anemia por deficiencia de hierro')
    elif validar_cualquier_opcion('Por deficiencia de vitaminas'):
        print('Tiene anemia por deficiencia de vitaminas')
    else:
        print('No cumple con las reglas de los tipos de anemia')
