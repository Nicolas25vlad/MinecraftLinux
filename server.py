import asyncio
import websockets
import os
from pathlib import Path
from user import linuxRemotoOneTime


class LinuxCommandWebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.connected_clients = set()
        
    async def read_output_file(self):
        """Lê o conteúdo do arquivo de saída"""
        try:
            file_path = "saida_terminal_linux.txt"
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            else:
                return "Arquivo de saída não encontrado"
        except Exception as e:
            return f"Erro ao ler arquivo de saída: {str(e)}"
    
    async def process_command(self, input_string):
        """Processa o comando e retorna o resultado"""
        try:
            # Chama seu método estático (ajuste conforme necessário)
            
            # Executa o método
            resultado = linuxRemotoOneTime(input_string)
            
            # Aguarda para garantir que o arquivo foi salvo
            await asyncio.sleep(0.5)
            
            # Lê o conteúdo do arquivo gerado
            file_content = await self.read_output_file()
            return file_content
            
        except Exception as e:
            return f"Erro ao processar comando: {str(e)}"
    
    async def handler(self, websocket):
        """Manipula cada conexão de cliente"""
        self.connected_clients.add(websocket)
        print(f"Cliente conectado. Total: {len(self.connected_clients)}")
        
        try:
            async for message in websocket:
                print(f"Comando recebido: {message}")
                
                # Processa o comando
                resultado = await self.process_command(message)
                
                # Envia o resultado
                await websocket.send(resultado)
                print("Resultado enviado para o cliente")
                    
        except websockets.exceptions.ConnectionClosed:
            print("Cliente desconectado")
        finally:
            self.connected_clients.remove(websocket)
    
    async def start_server(self):
        """Inicia o servidor WebSocket"""
        print(f"Servidor Linux WebSocket iniciado em ws://{self.host}:{self.port}")
        
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()


async def start():
    # Escolha a versão que melhor se adapta ao seu código
    linuxRemotoOneTime("echo 'Linux iniciado'")
    server = LinuxCommandWebSocketServer(host='localhost', port=8765)
    await server.start_server()