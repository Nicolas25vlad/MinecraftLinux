from linux import DockerTerminalReal




def linux():
    arquivo = "saida_terminal_linux.txt"
    terminal = DockerTerminalReal()
    tela = terminal.executar("echo 'Linux iniciado'")
    salvar_saida_em_arquivo(arquivo, tela)
    print(tela)
    # Usa o método principal
    while True:
        salvar_saida_em_arquivo(arquivo, terminal._get_prompt())
        comand = input(terminal._get_prompt())
        salvar_saida_em_arquivo(arquivo, terminal._get_prompt()+comand)
        tela = terminal.executar(comand)
        salvar_saida_em_arquivo(arquivo, tela)
        if comand.lower() in ['exit', 'quit']:
            terminal.exit()
            break
        else:
            if tela != "":
                print(tela)





def salvar_saida_em_arquivo(nome_arquivo, string):
    """
    Salva a saída capturada do terminal em um arquivo de texto.
    """
    if string!= "":
        with open(nome_arquivo, 'a') as arquivo:
            arquivo.write(string + '\n')




def linuxRemotoOneTime(string):
    arquivo = "saida_terminal_linux.txt"
    terminal = DockerTerminalReal()
    # Usa o método principal
    comand = string
    salvar_saida_em_arquivo(arquivo, terminal._get_prompt()+comand)
    tela = terminal.executar(comand)
    salvar_saida_em_arquivo(arquivo, tela)
    salvar_saida_em_arquivo(arquivo, terminal._get_prompt())
    if comand.lower() in ['exit', 'quit']:
        terminal.exit()
    return