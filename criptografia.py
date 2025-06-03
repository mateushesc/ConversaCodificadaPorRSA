from RSA import gerarE, totienteDeEuler, gerarD, RSACriptografiaString,RSADescriptografiaString, p, q
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


def criptografia_mensagem(mensagem, e_recebido, n_recebido):

    assinatura = str(assinar_mensagem(mensagem, d, n))
    mensagem_criptografada = RSACriptografiaString(mensagem, e_recebido, n_recebido)

    return mensagem_criptografada + "#" + assinatura


def descriptografia_mensagem(mensagemCriptografada, e_recebido, n_recebido):

    mensagem, assinatura = mensagemCriptografada.split("#")
    assinatura = int(assinatura)
    mensagem = RSADescriptografiaString(mensagem, p, q, d)

    if verificar_assinatura(mensagem, assinatura, e_recebido, n_recebido):
        return mensagem
    
    return

# Chamadas para teste

'''
mensagem = "Mensagem muito importante!"
'''

'''
# 1. Assinar
assinatura = assinar_mensagem(mensagem, d, n)
print("Assinatura:", assinatura)
s
# 2. Verificar
verificada = verificar_assinatura(mensagem, assinatura, e, n)
print("Assinatura válida?", verificada)
'''

'''
mensagemProntaParaMandar = criptografia_mensagem(mensagem, d, n)

print("Mensagem pronta para Webhooks:", mensagemProntaParaMandar)

mensagemOriginalVerificada = descriptografia_mensagem(mensagemProntaParaMandar)

print("Mensagem original verificada:", mensagemOriginalVerificada)
'''


