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
    
    mensagem_bytes = mensagem.encode('utf-8')
    mensagem_int = int.from_bytes(mensagem_bytes, byteorder='big')
    
    return pow(mensagem_int, e, n)

def descriptografia(mensagemCriptografada, d, n):
    
    mensagemDescriptografada = pow(mensagemCriptografada, d, n)
    
    mensagem_bytes = mensagemDescriptografada.to_bytes((mensagemDescriptografada.bit_length() + 7) // 8, byteorder='big')
    
    return mensagem_bytes.decode('utf-8')
    
    
# Chamadas para teste

ϕn = totienteDeEuler(p, q)
e = gerarE(ϕn)
#print("E é igual:", e)
d = gerarD(ϕn, e)
#print("D é igual:", d)

mensagem = "Muito obrigado por tudo"

mensagemCriptografada = criptografia(mensagem, e, n)
mensagemDescriptografada = descriptografia(mensagemCriptografada, d, n)
print(mensagemDescriptografada)

