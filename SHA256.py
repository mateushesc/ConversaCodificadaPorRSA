import struct

# Valores iniciais do hash (raízes quadradas dos 8 primeiros primos)
H_inicial = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

# Vetor de constantes K, derivadas das partes fracionárias das raízes cúbicas dos 64 primeiros primos
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def padding(mensagem):
    
    # Codifica a mensagem como bytes (UTF-8)
    mensagemBytes = mensagem.encode('utf-8')
    # Calcula o comprimento da mensagem original em bits
    comprimentoMensagem = len(mensagemBytes) * 8
    # Converte os bytes para uma string binária
    mensagemBinário = ''.join(f'{byte:08b}' for byte in mensagemBytes)
    
    # Adiciona o bit '1' (padding inicial)
    MensagemPadded = mensagemBinário + '1'
    
    # Adiciona bits '0' até que o tamanho da mensagem seja 64 bits a menos que um múltiplo de 512
    while (len(MensagemPadded) + 64) % 512 != 0:
        MensagemPadded += '0'
    
    # Adiciona 64 bits finais representando o comprimento original da mensagem
    comprimentoBinário = f'{comprimentoMensagem:064b}'
    MensagemPadded += comprimentoBinário
    
    return MensagemPadded

# Dividir a mensagem em blocos de 512 bits
def separaçãoBlocos(string, blocoSize = 512):
    return [string[i:i + blocoSize] for i in range(0, len(string), blocoSize)]

# Rotação para a direita de um inteiro de 32 bits
def rotaçãoDireita(valor, bits):
    return ((valor >> bits) | (valor << (32 - bits))) & 0xFFFFFFFF

def Ch(x, y, z): # Escolhe bits baseados em x
    return (x & y) ^ (~x & z)

def Maj(x, y, z): # Maioria dos bits
    return (x & y) ^ (x & z) ^ (y & z)

def Sigma0(x): # Função de rotação Σ₀
    return rotaçãoDireita(x, 2) ^ rotaçãoDireita(x, 13) ^ rotaçãoDireita(x, 22)

def Sigma1(x): # Função de rotação Σ₁
    return rotaçãoDireita(x, 6) ^ rotaçãoDireita(x, 11) ^ rotaçãoDireita(x, 25)

def rodadasDeCompressao(w, h_inicial):
    # Inicializa variáveis temporárias com os valores do hash atual
    a, b, c, d, e, f, g, h = h_inicial

    for i in range(64):
        # Calcula os valores temporários
        S1 = Sigma1(e)
        ch = Ch(e, f, g)
        temp1 = (h + S1 + ch + K[i] + w[i]) & 0xFFFFFFFF

        S0 = Sigma0(a)
        maj = Maj(a, b, c)
        temp2 = (S0 + maj) & 0xFFFFFFFF

        # Atualiza os valores das variáveis
        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF
        
    # Retorna os valores após a compressão do bloco
    return [a, b, c, d, e, f, g, h]

# Soma os valores anteriores com os novos e mantém 32 bits
def atualizarHash(H_inicial, H_temp):
    return [(x + y) & 0xFFFFFFFF for x, y in zip(H_inicial, H_temp)]

# Concatena os 8 valores em hexadecimal, com 8 dígitos cada
def gerar_hash_final(H):
    return ''.join(f'{h:08x}' for h in H)

def gerarPalavras256(bloco):
    
    # Divide o bloco de 512 bits em 16 palavras de 32 bits
    palavras = [int(bloco[i:i +32], 2) for i in range (0, 512, 32)]
    
    # Expande para 64 palavras com funções sigma
    for i in range(16, 64):
        s0 = rotaçãoDireita(palavras[i - 15], 7) ^ rotaçãoDireita(palavras[i - 15], 18) ^ (palavras[i - 15] >> 3)
        s1 = rotaçãoDireita(palavras[i - 2], 17) ^ rotaçãoDireita(palavras[i - 2], 19) ^ (palavras[i - 2] >> 10)
        novaPalavra = (palavras[i - 16] + s0 + palavras[i - 7] + s1) & 0xFFFFFFFF
        palavras.append(novaPalavra)
        
    return palavras

def sha256(mensagem):
    
    # Realiza o padding e divide em blocos de 512 bits
    padded = padding(mensagem)
    blocos = separaçãoBlocos(padded)

    # Processa cada bloco
    for bloco in blocos:
        w = gerarPalavras256(bloco)
        H_temp = rodadasDeCompressao(w, H_inicial)
        H = atualizarHash(H_inicial, H_temp)
        
    # Gera o hash final concatenado em hexadecimal
    return gerar_hash_final(H)