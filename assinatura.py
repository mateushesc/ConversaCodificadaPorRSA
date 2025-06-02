from RSA import gerarE, totienteDeEuler, gerarD, p, q
from SHA256 import sha256

ϕn = totienteDeEuler(p, q)
e = gerarE(ϕn)
d = gerarD(ϕn, e)
n = p * q  # Já declarado

def assinar_mensagem(mensagem, d, n):
    hash_mensagem = sha256(mensagem)
    hash_int = int(hash_mensagem, 16)  # SHA-256 gera hash de 256 bits
    assinatura = pow(hash_int, d, n)   # RSA com chave privada
    return assinatura

def verificar_assinatura(mensagem, assinatura, e, n):
    hash_calculado = sha256(mensagem)
    hash_calculado_int = int(hash_calculado, 16)

    hash_assinatura = pow(assinatura, e, n)  # RSA com chave pública

    return hash_calculado_int == hash_assinatura

mensagem = "Mensagem muito importante!"

# 1. Assinar
assinatura = assinar_mensagem(mensagem, d, n)
print("Assinatura:", assinatura)

# 2. Verificar
verificada = verificar_assinatura(mensagem, assinatura, e, n)
print("Assinatura válida?", verificada)




