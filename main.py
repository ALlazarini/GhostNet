from network import Network
import algorithms
import incident
import os

def display_hud(network):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    print("       GHOSTNET - MONITORAMENTO URBANO       ")
    print("="*50)
    print(f"{'ID':<10} | {'TIPO':<15} | {'STATUS':<15}")
    print("-" * 50)
    
    for node_id in sorted(network.nodes.keys()):
        node = network.nodes[node_id]
        status_text = node.status.upper()
        if node.stability_timer > 0:
            status_text += f" ({node.stability_timer}T)"
        
        color = incident.COLORS.get(node.status, incident.COLORS["reset"])
        print(f"{node_id:<10} | {node.type:<15} | {color}{status_text:<15}{incident.COLORS['reset']}")
    
    print("-" * 50)
    print("ÚLTIMOS EVENTOS:")
    
    for log in incident.event_logs:
    
        print(log)
    
    print("-" * 50)
    print("1. Simular Falha | 2. Restaurar | 3. Conectividade (BFS) | \n 4. Buscar nos Logs (Rabin-Karp) | 5. Comprimir Logs (Huffman)| 6. Mapear Zonas (DFS) |\n 7. Calcular Rota (Dijkstra)|8. AGM | 9. TopoSort | 0. Sair")

def setup_initial_network():

    gn = Network()
    gn.add_node("hub-01", "Central Hub")
    gn.add_node("relay-01", "Relay Norte")
    gn.add_node("relay-02", "Relay Sul")
    gn.add_node("gate-01", "Gateway")
    gn.add_node("stor-01", "Data Storage")
    gn.add_node("back-01", "Backup Node")
    gn.add_connection("hub-01", "relay-01", 2)
    gn.add_connection("hub-01", "relay-02", 2)
    gn.add_connection("relay-01", "gate-01", 5)
    gn.add_connection("relay-02", "stor-01", 3)
    gn.add_connection("stor-01", "back-01", 1)
  
    return gn

if __name__ == "__main__":

    ghost_net = setup_initial_network()
    incident.add_log("Sistema GhostNet iniciado.", "log_info")
    
    while True:

        display_hud(ghost_net)
        opcao = input("\nGhostNet > ")

        if opcao == "1":
        
            node_id = input("ID do alvo: ")
            incident.apply_incident(ghost_net, node_id)
        
        elif opcao == "2":
            
            node_id = input("ID para restaurar: ")
            
            if node_id in ghost_net.nodes:
            
                ghost_net.nodes[node_id].status = "normal"
                ghost_net.nodes[node_id].stability_timer = -1
                incident.add_log(f"SISTEMA: {node_id} restaurado.", "log_info")
        
        elif opcao == "3":
            
            start_node = "hub-01"
            reachable = algorithms.bfs_reachability(ghost_net, start_node)
            isolated = [node_id for node_id in ghost_net.nodes if node_id not in reachable]
            
            print(f"\n--- ANÁLISE DE CONECTIVIDADE (FONTE: {start_node}) ---")
            print(f"ACESSÍVEIS: {', '.join(sorted(reachable))}")
            print(f"ISOLADOS: {', '.join(sorted(isolated))}")
            input("\nPressione Enter para continuar...")
        
        elif opcao == "4":
        
            term = input("\nTermo de busca: ")
            print(f"\n--- BUSCA EM LOGS ---")
        
            for log in incident.event_logs:
            
                clean_log = log.replace("\033[91m","").replace("\033[93m","").replace("\033[94m","").replace("\033[0m","")
            
                if algorithms.rabin_karp(clean_log.lower(), term.lower()):
                    print(log)
        
            input("\nPressione Enter...")

        elif opcao == "5":
        
            full_text = "".join(incident.event_logs)
        
            if full_text:
        
                compressed, _ = algorithms.huffman_compress(full_text)
                original_bits = len(full_text) * 8
                comp_bits = len(compressed)
                print(f"\n--- COMPRESSÃO HUFFMAN ---")
                print(f"Original: {original_bits} bits | Comprimido: {comp_bits} bits")
                print(f"Economia: {(1 - (comp_bits/original_bits))*100:.2f}%")

            input("\nPressione Enter...")    

        # o comando res é pra resetar os distritos e poder consultar os logs sem tudo explodir no processo, nn aparece no menu justamente
        # pra ser tipo um comando de admin

        elif opcao == "res":
            for node_id in ghost_net.nodes:
                node = ghost_net.nodes[node_id]
                node.status = "normal"
                node.stability_timer = -1
            
            incident.add_log("SISTEMA: Restauração total da rede executada.", "log_info")
            print("\n[!] Comando Fantasma: Todos os distritos estão ONLINE.")
            input("Pressione Enter para continuar...") 

        elif opcao == "6":
            islands = algorithms.dfs_islands(ghost_net)
            
            print("\n--- MAPEAMENTO DE ZONAS (DFS) ---")
            if not islands:
                print("[!] BLACKOUT TOTAL: Nenhum distrito operacional.")
            else:
                for i, island in enumerate(islands, 1):
                    print(f"Zona Operacional {i}: {', '.join(sorted(island))}")
            
            input("\nPressione Enter para continuar...")   

        elif opcao == "7":
            start = input("ID do nó de origem: ")
            end = input("ID do nó de destino: ")
            
            path, cost = algorithms.dijkstra_shortest_path(ghost_net, start, end)
            
            print(f"\n--- CÁLCULO DE ROTA ({start} -> {end}) ---")
            if path:
                print(f"Caminho: {' -> '.join(path)}")
                print(f"Custo Total: {cost}")
            else:
                print("[!] ROTA INVIÁVEL: Destino inalcançável ou bloqueado por nós offline.")
            
            input("\nPressione Enter para continuar...")  

        elif opcao == "8":
            start_node = "hub-01"
            edges, cost = algorithms.agm_prim(ghost_net, start_node)
            
            print("\n--- ÁRVORE GERADORA MÍNIMA (AGM) ---")
            if edges:
                for frm, to, w in edges:
                    print(f"{frm} <-> {to} (Custo: {w})")
                print(f"Custo Mínimo de Reconexão: {cost}")
            else:
                print("[!] Não foi possível gerar a rede.")
            input("\nPressione Enter para continuar...")

        elif opcao == "9":
            deps = {
                "hub-01": ["relay-01", "relay-02"],
                "relay-01": ["gate-01"],
                "relay-02": ["stor-01"],
                "stor-01": ["back-01"],
                "gate-01": [],
                "back-01": []
            }
            order = algorithms.recovery_toposort(deps)
            
            print("\n--- ORDEM LÓGICA DE RECUPERAÇÃO (TOPOSORT) ---")
            if order:
                print(" -> ".join(order))
            else:
                print("[!] Ciclo detectado, ordem inviável.")
            input("\nPressione Enter para continuar...")    

        elif opcao == "0":
            break
        
        incident.process_turn(ghost_net)