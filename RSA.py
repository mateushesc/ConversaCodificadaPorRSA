import random
import math

#Parte 1 [x]
#Parte 2 [x]
#Parte 3 [x]
#Parte 4 [x]
#Parte 5 [x]
#Parte 6 []
#Parte 7 []

# Parametros
bits = 8
seed = 12345

#Parte 1: Escolha dos números primos

#    Gerar dois números primos grandes: p e q
#============================================================================================

# Algoritmo simples de teste de primalidade (Miller-Rabin pode ser usado depois para mais segurança)
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return False
    return True

# Gerador de número primo aleatório com um número fixo de bits
def generate_prime_candidate(bits):
    return random.getrandbits(bits) | 1 | (1 << (bits - 1))  # garante que é ímpar e tem tamanho certo

def generate_prime(bits):
    while True:
        candidate = generate_prime_candidate(bits)
        if is_prime(candidate):
            return candidate

# Função principal para gerar dois primos com seed
def generate_two_primes(bits, seed):
    random.seed(seed)
    p = generate_prime(bits)
    q = generate_prime(bits)
    # Garante que p e q sejam diferentes
    while q == p:
        q = generate_prime(bits)
    return p, q



#Parte 2: Cálculo de parâmetros principais

#    Calcular n = p × q

#    Calcular o totiente de Euler: φ(n) = (p - 1) × (q - 1)
#=============================================================================================

def calculoParametros(p, q):
    n = p * q
    # Totiente de Euler:
    φn = (p -1) * (q-1)
    return n, φn

#Parte 3: Geração da chave pública

#     Escolher um número e tal que:

#        1 < e < φ(n)

#        e é coprimo com φ(n) (mdc(e, φ(n)) = 1)
#=============================================================================================

def verificarCoprimo(n1, n2):
    return math.gcd(n1, n2) == 1

def gerarE(φn):
    e = random.randrange(2, φn)
    if verificarCoprimo(e, φn):
        return e

#Parte 4: Geração da chave privada

#    Calcular d, o inverso modular de e módulo φ(n)

#    Obter:

#        Chave pública: (n, e)

#        Chave privada: (n, d)
#=============================================================================================

def gerarD(e, φn):
    d, novo_d = 0, 1
    r, novo_r = φn, e

    while novo_r != 0:
        quociente = r // novo_r
        d, novo_d = novo_d, d - quociente * novo_d
        r, novo_r = novo_r, r - quociente * novo_r

    if r > 1:
        raise Exception("e não tem inverso modular")
    if d < 0:
        d = d + φn

    return d

# Parte 5: Criptografia

#    Converter a mensagem em número inteiro m, tal que 0 < m < n

#    Calcular o texto cifrado: c = m^e mod n
#=============================================================================================

def converterParaBinário(mensagem):
    binario = ''.join(format(ord(c), '08b') for c in mensagem)
    print(binario)
    return binario

def criptografiaDaMensagem(mensagem, e, n):

    mensagem = (converterParaBinário(mensagem))
    mensagem = int(mensagem, 2)

    mensagemCriptografada = pow(mensagem, e)
    mensagemCriptografada = mensagemCriptografada % n

    print(mensagemCriptografada)

    return mensagemCriptografada

#Parte 6: Descriptografia

#    Calcular a mensagem original: m = c^d mod n

#    Converter o número de volta para a mensagem original (texto)
#=============================================================================================

def descriptografiaDaMensagem(mensagemCriptografada, d, n):
    mensagem = pow(mensagemCriptografada, d)
    mensagem = mensagem % n

    print(bin(mensagem))

#Parte 7: Testes e validação

#    Verificar se m descriptografado é igual ao m original

#    Testar com diferentes tamanhos de primos e mensagens
#=============================================================================================


#Chamadas de funções
p, q = generate_two_primes(bits, seed)
print(f"Primo p: {p}")
print(f"Primo q: {q}")

n, φn = calculoParametros(p, q)
print("Totiente de euler é:", φn)

e = gerarE(φn)
print("Variável E é:", e)

d = gerarD(e, φn)
print("Variável D é:", d)

mensagem = "texto"

mensagemCriptografada = criptografiaDaMensagem(mensagem, e, n)

descriptografiaDaMensagem(mensagemCriptografada, d, n)