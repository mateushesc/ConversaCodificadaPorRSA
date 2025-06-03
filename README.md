# 🔐 Conversa Codificada por RSA

Este projeto simula uma comunicação segura utilizando criptografia **RSA** e assinatura digital com **SHA-256** (implementado manualmente). O objetivo é demonstrar como garantir **confidencialidade**, **autenticidade** e **integridade** de mensagens através de criptografia assimétrica e funções hash.

---

## ✨ Funcionalidades

- 🔑 Geração de par de chaves RSA (pública e privada)
- 🧮 Implementação manual do algoritmo SHA-256
- 🖊️ Assinatura digital de mensagens com SHA-256 + RSA
- 🔐 Criptografia e descriptografia de mensagens
- ✅ Verificação de assinaturas digitais

---

## 📁 Estrutura do Projeto

ConversaCodificadaPorRSA/
│
├── RSA.py # Implementação do algoritmo RSA
├── SHA256.py # Implementação do algoritmo SHA-256
├── conversa_codificada.py # Script principal que executa a comunicação segura
└── keys/
├── chave_privada.txt # Chave privada do remetente
└── chave_publica.txt # Chave pública do remetente


---

## ▶️ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/ConversaCodificadaPorRSA.git
   cd ConversaCodificadaPorRSA'

2. Execute o script principal:
    python conversa_codificada.py

---

## ⚙️ Requisitos
    Python 3.x
    Flask

---


## 📚 Conceitos Utilizados
    RSA: Criptografia assimétrica que permite proteger mensagens e validar remetentes

    SHA-256: Função hash segura usada para gerar resumos únicos de mensagens

    Assinatura Digital: Combinação de SHA-256 e RSA para garantir a integridade e autenticidade

---

## Autor
    Desenvolvido por Mateus Henrique Escolaro

