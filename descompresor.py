import bitarray as bit
from ast import literal_eval

def interpretacion_huff(huff_file):
    bits = bit.bitarray()
    with open (huff_file, mode = 'rb') as bf:
        bits.fromfile(bf)
    text = bits.to01()
    return text

def interpretacion_table(table_file):
    with open (table_file, mode = 'r') as file:
        codes = file.read()
        file.close()
    codes = literal_eval(codes)
    return codes

def descompresion(text,codes,new_file):
    characters = []
    routes = []
    for i in codes:
        characters += [i[0]]
        route = []
        for j in range (1,len(i)):
            route += [i[j]]
        routes.append(route)
    decodedtext = ""
    currentcode = []
    for x in range (len(text)):
        currentcode += [text[x]]
        if currentcode in routes:
            decodedtext += characters[routes.index(currentcode)]
            currentcode = []
    with open (new_file, mode = 'w') as file:
        file.write(decodedtext)
        file.close()
    


def main():
    huff_file, table_file, new_file = map(str, input().split())
    text = interpretacion_huff(huff_file)
    codes = interpretacion_table(table_file)
    descompresion(text,codes,new_file)

main()