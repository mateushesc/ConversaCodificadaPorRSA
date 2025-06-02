import math

p = 2213123628354983897115998625336689827687390117113653005630630027169371604551404890654628122259001177759
q = 1769642401523647528710653959246630370406623814212235550117706938766204256846730841459606269250539310923

n = p * q

def totienteDeEuler(p, q):
    return (p - 1) * (q - 1)
    
def gerarE(ϕn):
    e = 65537
    
    if math.gcd(e, ϕn) == 1:
        return e
    
    for e in range(3, ϕn, 2):
        if math.gcd(e, ϕn) ==1:
            return e
    
    raise ValueError("Falha ao achar valor válido para E")

def gerarD(ϕn, e):
    return pow(e, -1, ϕn)

def criptografia(mensagem, e, n):
    
    mensagemBytes = mensagem.encode('utf-8')
    mensagemInt = int.from_bytes(mensagemBytes, byteorder='big')
    
    return pow(mensagemInt, e, n)

def descriptografia(mensagemCriptografada, d, n):
    
    mensagemDescriptografada = pow(mensagemCriptografada, d, n)
    
    mensagemBytes = mensagemDescriptografada.to_bytes((mensagemDescriptografada.bit_length() + 7) // 8, byteorder='big')
    
    return mensagemBytes.decode('utf-8')

# Separação em blocos e reconstrução de blocos
# blocoSize = 21

def separaçãoBlocos(string, blocoSize):
    return [string[i:i + blocoSize] for i in range(0, len(string), blocoSize)]

def reconstruçãoBlocos(blocos):
    return ''.join(blocos)
    
# Chaves públicas (n, e)
# Chaves privadas (p, q, d)
    
def RSACriptografia(mensagem, e, n):
    
    blocos = separaçãoBlocos(mensagem, 21)
    
    blocosCriptografados = []
    
    for bloco in blocos:
        blocosCriptografados.append(criptografia(bloco, e, n))
        
    return blocosCriptografados

def RSADescriptografia(blocosCriptografados, p, q, d):
    
    n = p * q
    
    blocosDescriptografados = []
    
    for bloco in blocosCriptografados:
       blocosDescriptografados.append(descriptografia(bloco, d, n))
        
    return reconstruçãoBlocos(blocosDescriptografados)

# Chamadas para teste

ϕn = totienteDeEuler(p, q)
e = gerarE(ϕn)
#print("E é igual:", e)
d = gerarD(ϕn, e)
#print("D é igual:", d)

mensagem = """
Era uma vez, em um mundo digital, um estudante chamado Mateus que adorava desafios de criptografia. Ele estudava algoritmos como AES, RSA, Diffie-Hellman e ficava fascinado com a ideia de proteger mensagens secretas contra bisbilhoteiros curiosos. 

Em uma noite chuvosa, enquanto o trovão ecoava pela cidade, Mateus decidiu implementar sua própria versão do algoritmo RSA. "Será que consigo dividir mensagens em blocos, criptografar e depois recuperar tudo perfeitamente?", pensou. 

Ele escreveu função após função — para gerar primos gigantes, calcular o totiente de Euler, encontrar o expoente público 'e', o expoente privado 'd', e claro, converter mensagens entre strings, inteiros e de volta. Tudo parecia promissor.

Mas então... 💥 Um erro! Um simples caractere fora do padrão, um 'ã', fez tudo falhar. "Ah, os bytes malditos do UTF-8!", gritou ele com o teclado na mão e os olhos cheios de determinação. 

Sem desistir, ajustou o tamanho dos blocos, corrigiu a conversão dos inteiros e adicionou verificações para evitar que os números ultrapassassem 'n'. E finalmente, como num passe de mágica, a mensagem secreta voltou ilesa, como se nunca tivesse sido embaralhada por fórmulas matemáticas complexas.

Essa é a história de como a persistência codificou o sucesso — com matemática, coragem e um pouco de café.
"""

blocosCriptografados = RSACriptografia(mensagem, e, n)

#print(blocosCriptografados)

mensagemDescriptografada = RSADescriptografia(blocosCriptografados, p, q, d)

print(mensagemDescriptografada)

