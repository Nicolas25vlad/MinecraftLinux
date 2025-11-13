-- cliente.lua
local conexao = http.websocket("ws://localhost:8765")
if not conexao then print("Servidor offline") return end

if arg[1] then
    conexao.send(table.concat(arg, " "))
    local inicio = os.epoch("utc")
    while true do
        local r = conexao.receive()
        if r then print(r) break end
        if os.epoch("utc") - inicio > 30000 then print("Timeout") break end
        os.sleep(0.1)
    end
    conexao.close()
    return
end

term.clear()
print("Digite 'sair' para sair")

while true do
    write("> ")
    local cmd = read()
    if cmd == "sair" then break end
    if cmd == "clear" then term.clear() goto continue end
    
    conexao.send(cmd)
    local inicio = os.epoch("utc")
    while true do
        local r = conexao.receive()
        if r then 
            print(r) 
            break 
        end
        if os.epoch("utc") - inicio > 30000 then 
            print("Timeout") 
            break 
        end
        os.sleep(0.1)
    end
    ::continue::
end

conexao.close()
print("Conexao fechada")