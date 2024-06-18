import bitarray as bit

def contenido_archivo(fileName):
    with open(fileName,mode ='r') as file:
        Text = (file.read())
        file.close()
        return Text
    
def ascii(text):
    f = [0]*256
    for B in range (len(text)):
        f[ord(text[B])] += 1
    return f

def frequencias_caracteres(f):
    charfreq = []
    for i in range (len(f)):
        if f[i] != 0:
            charfreq.append([f[i],chr(i)])
    charfreq.sort(key=lambda x:x[0])
    return charfreq

def huffmantree(charfreq):
    while len(charfreq) != 1:
        leaf1 = charfreq[0]
        leaf2 = charfreq[1]
        sum = leaf1[0] + leaf2[0]
        if len(leaf1) == 3 and len(leaf2) == 3:
            charfreq.append([sum,leaf1,leaf2])
        elif len(leaf1) == 3:
            charfreq.append([sum,leaf1,[leaf2[1],[],[]]])
        elif len(leaf2) == 3:
            charfreq.append([sum,[leaf1[1],[],[]],leaf2])
        else:
            charfreq.append([sum,[leaf1[1],[],[]],[leaf2[1],[],[]]])
        charfreq.pop(0)
        charfreq.pop(0)
        charfreq.sort(key=lambda x:x[0])
    return charfreq[0]
        
def codigos(T,name,camino = [],res = []):
    v,I,D = T
    if I == [] and D == []:
        camino.insert(0,v)
        res.append(camino)
        return res
    if I != []:
        codigos(I,name,camino+['0'],res)
    if D != []:
        codigos(D,name,camino+['1'],res)
    with open(name+'.table','w') as file:
        file.write(str(res))
        file.close()
    return res

def compresion(text,caminos,name):
    textocompreso = ""
    for i in range (len(text)):
        for j in range (len(caminos)):
            if caminos[j][0] == text[i]:
                for x in range (1,len(caminos[j])):
                    textocompreso += str(caminos[j][x])
    bits = bit.bitarray(textocompreso)
    with open(name+'.huff',mode = 'wb') as bf:
        bits.tofile(bf)
    return bits

def altura_arbol(arbol):
    if isinstance(arbol, list) and len(arbol) == 3:
        izquierda = arbol[1]
        derecha = arbol[2]
        return 1 + max(altura_arbol(izquierda), altura_arbol(derecha))
    else:
        return -1
    
def anchura_arbol(arbol):
    if not isinstance(arbol, list) or len(arbol) == 0:
        return 0
    nivel_actual = [arbol]
    max_anchura = 0
    
    while nivel_actual:
        nivel_actual_siguiente = []
        count = 0
        
        for nodo in nivel_actual:
            count += 1
            
            if isinstance(nodo, list) and len(nodo) == 3:
                nivel_actual_siguiente.extend(nodo[1:])
        
        max_anchura = max(max_anchura, count)
        nivel_actual = nivel_actual_siguiente
    
    return max_anchura

def nodos_por_nivel(arbol):
    if not arbol:
        return []
    niveles = []
    nivel_actual = [arbol]
    while nivel_actual:
        niveles.append(len(nivel_actual)) 

        siguiente_nivel = []
        for nodo in nivel_actual:
            if len(nodo) > 1 and nodo[1]:
                siguiente_nivel.append(nodo[1])
            if len(nodo) > 2 and nodo[2]:
                siguiente_nivel.append(nodo[2])
        nivel_actual = siguiente_nivel

    return niveles


def escribir_resultados_en_archivo(filename, Text, funciones, tree):
    nombre_salida = f"{filename}.stats"
    with open(nombre_salida, 'w') as file:
        file.write(f"Árbol original : {tree}\n")
        file.write(f"Altura del árbol : {funciones[0]}\n")
        file.write(f"Anchura del árbol : {funciones[1]}\n")
        file.write(f"Cantidad de nodos por nivel: {funciones[2]}\n")
        file.write(f"Tabla de frecuencias original: {Text}")



def main():
    fileName = str(input())
    Text = contenido_archivo(fileName)
    Frequency = ascii(Text)
    charfreq = frequencias_caracteres(Frequency)
    charfreq2 = frequencias_caracteres(Frequency)
    Tree = (huffmantree(charfreq))
    Routes = (codigos(Tree,fileName))
    compresion(Text,Routes,fileName)
    funciones = [altura_arbol(Tree), anchura_arbol(Tree), nodos_por_nivel(Tree)]
    escribir_resultados_en_archivo(fileName,charfreq2, funciones, Tree)    
    
main()


