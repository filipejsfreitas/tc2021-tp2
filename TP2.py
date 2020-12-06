from pprint import pprint
from collections import OrderedDict


lines = []


with open('tp2-ciphertexts.txt', mode='r') as file:
    lines = [x.strip() for x in filter(lambda x: len(x.strip()) > 0, file.readlines())]


def sxor(s1, s2):
    # Implementação simples da função de decifragem: (A-B) % 26
    # Aceita duas strings e faz a "decifragem" de ambas as strings, caracter a caracter,
    # retornando uma nova string correspondente à decifragem
    return ''.join(chr(((ord(a) - ord('A')) - (ord(b) - ord('A')) % 26) + ord('A')) for a, b in zip(s1, s2))


def frequency_analysis_blocks(cryptogram, n = 2):
    # Faz uma análise de frequências num dado criptograma
    # O parâmetro n define o tamanho dos blocos sobre os quais a análise vai ser feita
    # Por exemplo: se quisermos fazer análise de frequências em todos os digrafos, basta fazer n=2
    # Para uma análise de frequências dos caracteres individuais do criptograma, n=1
    # Esta função ignora espaços e outros caracteres equivalentes
    # No final, a função retorna um dicionário ordenado com a correspondência caracter: frequência.
    # A ordem é do caracter mais frequente para o menos frequente.

    frequencies = {}
    total_blocks = 0
    
    for i in range(0, len(cryptogram)):
        c = cryptogram[i:i+n]

        if c.isspace():# or not c.isalpha():
            continue
        
        if c not in frequencies:
            frequencies[c] = 0
        
        frequencies[c] += 1
        total_blocks += 1
    
    for c, f in frequencies.items():
        frequencies[c] = round(f / total_blocks, 3)
    
    return OrderedDict(sorted(frequencies.items(), reverse=True, key=lambda x: x[1]))


xors = {}

# Para cada par de criptogramas, vamos descobrir qual é o seu xor e guardar no dicionário acima
for i in range(len(lines)):
    for j in range(i + 1, len(lines)):
        if i == j:
            continue

        x = lines[i]
        y = lines[j]
        
        xors[(x, y)] = (sxor(x, y))


# Para cada xor, vamos fazer uma análise de frequências nos seus caracteres
frequencies = OrderedDict(sorted({xor: list(frequency_analysis_blocks(xor, 1).items()) for xor in xors.values()}.items(), key = lambda x: x[1][0][1], reverse=True))
# Imprimir o top 5 dos caracteres mais frequentes em cada xor
pprint([x[:5] for x in frequencies.values()])

# O xor correto, i.e., o xor correspondente aos dois criptogramas cifrados com a mesma chave, é o primeiro da lista
# de frequências calculada acima, visto que esta está ordenada por frequências descendentes
xor_correto = list(frequencies.items())[0][0]
print(xor_correto)

# Descobrir quais os índices dos criptogramas que deram origem ao xor correto
a, b = None, None
for (x, y), xor in xors.items():
    if xor == xor_correto:
        a, b = lines.index(x), lines.index(y)

# Imprimir os índices, seguido do texto criptogramas corretos
print(a, b, '\n\n')
print(lines[a], '\n\n', lines[b])
