import docker

class DockerTerminalReal:
    def __init__(self, image="ubuntu:latest"):
        self.client = docker.from_env()
        self.image = image
        self.container = None
        self.current_dir = "/"
        self._start_container()
    
    def _start_container(self):
        """Inicia o container com prompt colorido"""
        self.container = self.client.containers.run(
            self.image,
            command="tail -f /dev/null",
            detach=True,
            tty=True
        )
        
        # Configura prompt colorido
        setup_cmd = """
        echo 'export PS1="\\[\\033[1;32m\\]\\u@docker\\[\\033[0m\\]:\\[\\033[1;34m\\]\\w\\[\\033[0m\\]\\$ "' >> ~/.bashrc
        """
        self.container.exec_run(["bash", "-c", setup_cmd])
        
        result = self.container.exec_run(["bash", "-c", "pwd"])
        self.current_dir = result.output.decode('utf-8').strip()
    
    def _get_prompt(self):
        """Retorna prompt colorido"""
        return f"root@docker:{self.current_dir}# "
    
    def executar(self, comando):
        """
        MÉTODO PRINCIPAL - Retorna apenas a saída do comando
        """
        try:
            # Atualiza o diretório se for comando cd
            if comando.strip().startswith('cd '):
                novo_dir = comando.strip()[3:].strip()
                result = self.container.exec_run(
                    ["bash", "-c", f"cd {self.current_dir} && cd {novo_dir} 2>/dev/null && pwd || echo ERROR"]
                )
                output = result.output.decode('utf-8').strip()
                
                if output != "ERROR":
                    self.current_dir = output
                    return ""  # cd bem-sucedido não tem saída
                else:
                    return f"bash: cd: {novo_dir}: No such file or directory"
            
            # Para outros comandos - executa no diretório atual
            result = self.container.exec_run(
                ["bash", "-c", f"cd {self.current_dir} && {comando}"],
                demux=True
            )
            
            exit_code, (stdout, stderr) = result
            
            # Combina apenas a saída do comando
            output = ""
            
            if stdout:
                output += stdout.decode('utf-8', errors='replace')
            if stderr:
                stderr_text = stderr.decode('utf-8', errors='replace')
                if stderr_text:
                    if output and not output.endswith('\n'):
                        output += '\n'
                    output += stderr_text
            
            return output.strip()
        except Exception as e:
            return f"Erro: {str(e)}"
    
    def exit(self):
        # encerra o programa mas mantém o container ativo
        pass
        
    def fechar(self):
        if self.container:
            self.container.stop()
            self.container.remove()

# EXEMPLO DE USO
if __name__ == "__main__":
    terminal = DockerTerminalReal()
    
    print("🎯 SIMULAÇÃO DE TERMINAL REAL")
    print("Cada comando mostra a linha completa como no CMD/PowerShell!\n")
    
    # Simula uma sessão
    comandos = [
        "ls -la",
        "pwd", 
        "cd /tmp",
        "pwd",
        "mkdir teste_dir",
        "ls -l",
        "cd teste_dir",
        "echo 'Arquivo de teste' > teste.txt",
        "cat teste.txt",
        "cd ..",
        "rm -rf teste_dir",
        "ls -l"
    ]
    
    for cmd in comandos:
        print("-" * 50)
        tela = terminal.executar(cmd)
        print(tela)
        print()
    
    terminal.fechar()