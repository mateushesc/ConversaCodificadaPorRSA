import requests
from flask import Flask, request, jsonify
import threading
from criptografia import criptografia_mensagem, descriptografia_mensagem

class ChatApplication:
    def __init__(self, name, port, target_port):
        self.name = name
        self.port = port
        self.target_port = target_port
        self.received_keys = {}  # {app_name: {'e': e, 'n': n}}
        self.app = Flask(name)
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/webhook', methods=['POST'])
        def webhook():
            data = request.json
            sender = data.get('sender')
            message = data.get('message')
            e = data.get('e')
            n = data.get('n')
            
            # Armazena chaves se recebidas
            if e and n:
                self.received_keys[sender] = {'e': e, 'n': n}
                print(f"\n[INFO] Chaves públicas recebidas de {sender}")
            
            # Processa mensagem se recebida
            if message and sender in self.received_keys:
                keys = self.received_keys[sender]
                decrypted = descriptografia_mensagem(message, keys['e'], keys['n'])
                if decrypted is not None:
                    print(f"\n[{sender}]: {decrypted}")
                else:
                    print(f"\n[ERRO] Falha ao descriptografar mensagem de {sender}")
            
            return jsonify({'status': 'received'}), 200
    
    def run_server(self):
        print(f"\n{self.name} rodando na porta {self.port}")
        self.app.run(port=self.port)
    
    def send_message(self, message, my_keys=None):
        target_url = f"http://localhost:{self.target_port}/webhook"
        payload = {
            'sender': self.name,
            'message': None
        }
        
        # Envia chaves se fornecidas
        if my_keys:
            payload['e'] = my_keys['e']
            payload['n'] = my_keys['n']
        
        # Criptografa mensagem se tiver chaves do destinatário
        if message:
            target_name = f"App{2 if self.name == 'App1' else 1}"
            if target_name in self.received_keys:
                keys = self.received_keys[target_name]
                encrypted = criptografia_mensagem(message, keys['e'], keys['n'])
                payload['message'] = encrypted
            else:
                print("\n[ERRO] Chaves públicas do destinatário não disponíveis. Envie suas chaves primeiro.")
                return
        
        try:
            response = requests.post(
                target_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=2
            )
            if response.status_code != 200:
                print(f"\n[ERRO] Falha ao enviar mensagem: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"\n[ERRO] Não foi possível conectar ao destinatário: {e}")

def main():
    # Configuração da App1
    app = ChatApplication("App1", 5000, 5001)
    
    # Chaves públicas de exemplo (substitua pelas suas)
    my_keys = {'e': 65537, 'n': 3916437412550842102727935875850855693553519166552686503146906891256559035530452921719207586458637703887960839810757967653426478394449576405419020812956388501828689669931660057986640427007324380985293361557}
    
    # Inicia o servidor em uma thread separada
    server_thread = threading.Thread(target=app.run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Pequena pausa para o servidor iniciar
    import time
    time.sleep(1)
    
    # Envia chaves públicas para a App2
    print("\nEnviando chaves públicas para App2...")
    app.send_message(None, my_keys)
    
    # Interface de chat simples
    print("\nChat iniciado (digite 'sair' para encerrar)")
    while True:
        message = input(f"[{app.name}]: ")
        if message.lower() == 'sair':
            break
        app.send_message(message)

if __name__ == "__main__":
    main()