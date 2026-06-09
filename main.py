from network import Network
import algorithms
import incident
import os
import threading
import time
import random

def start_chaos_clock(network):
    while True:
        time.sleep(15)
        operacionais = [n for n, obj in network.nodes.items() if obj.status == "normal"]
        if operacionais:
            alvo = random.choice(operacionais)
            incident.apply_incident(network, alvo)
            network.export_to_json()

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
    print("1. Falha | 2. Restaurar | 3. BFS | 4. Busca | 5. Huffman | 6. DFS | 7. Rota | 8. AGM | 9. TopoSort | 10. DP | 0. Sair")

def setup_initial_network():
    gn = Network()
    
    gn.add_node("hub-01", "Central Hub", x=640, y=360)
    gn.add_node("relay-01", "Relay Norte", x=640, y=160)
    gn.add_node("relay-02", "Relay Sul", x=640, y=560)
    gn.add_node("gate-01", "Gateway", x=340, y=160)
    gn.add_node("stor-01", "Data Storage", x=940, y=560)
    gn.add_node("back-01", "Backup Node", x=1140, y=560)
    
    gn.add_connection("hub-01", "relay-01", 2)
    gn.add_connection("hub-01", "relay-02", 2)
    gn.add_connection("relay-01", "gate-01", 5)
    gn.add_connection("relay-02", "stor-01", 3)
    gn.add_connection("stor-01", "back-01", 1)
    
    gn.export_to_json()
    return gn

if __name__ == "__main__":
    ghost_net = setup_initial_network()
    incident.add_log("Sistema GhostNet iniciado.", "log_info")

    relogio_caos = threading.Thread(target=start_chaos_clock, args=(ghost_net,), daemon=True)
    relogio_caos.start()
    
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
            input("\nPressione Enter para continuar...")

        elif opcao == "5":
            full_text = "".join(incident.event_logs)
            if full_text:
                compressed, _ = algorithms.huffman_compress(full_text)
                original_bits = len(full_text) * 8
                comp_bits = len(compressed)
                print(f"\n--- COMPRESSÃO HUFFMAN ---")
                print(f"Original: {original_bits} bits | Comprimido: {comp_bits} bits")
                print(f"Economia: {(1 - (comp_bits/original_bits))*100:.2f}%")
            input("\nPressione Enter para continuar...")

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
            
            ghost_net.clear_highlights()
            
            print(f"\n--- CÁLCULO DE ROTA ({start} -> {end}) ---")
            if path:
                print(f"Caminho: {' -> '.join(path)}")
                print(f"Custo Total: {cost}")
                
                for i in range(len(path) - 1):
                    ghost_net.highlighted_edges.append([path[i], path[i+1]])
            else:
                print("[!] ROTA INVIÁVEL: Destino inalcançável ou bloqueado por nós offline.")
                
            ghost_net.export_to_json()
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

        elif opcao == "10":
            offline_nodes = [node_id for node_id, node in ghost_net.nodes.items() if node.status == "offline"]
            
            ghost_net.clear_highlights()
            
            if not offline_nodes:
                print("\n[!] A rede está operacional. Sem alvos para recuperação.")
            else:
                try:
                    budget = int(input("\nOrçamento de Manutenção: "))
                except ValueError:
                    budget = 0
                
                costs = [25 if ghost_net.nodes[n].type == "Central Hub" else 10 for n in offline_nodes]
                values = [100 if ghost_net.nodes[n].type == "Central Hub" else 40 for n in offline_nodes]
                
                max_value, selected = algorithms.knapsack_recovery(offline_nodes, costs, values, budget)
                
                print("\n--- PLANEJAMENTO DE RECUPERAÇÃO (KNAPSACK DP) ---")
                print(f"Orçamento Disponível: {budget}")
                
                custo_gasto = sum(costs[offline_nodes.index(n)] for n in selected)
                print(f"Custo Utilizado: {custo_gasto}")
                print(f"Valor Estratégico Máximo: {max_value}")
                
                if selected:
                    print(f"Consertar Prioritariamente: {', '.join(selected)}")
                    ghost_net.highlighted_nodes = selected
                else:
                    print("Orçamento insuficiente para realizar manutenções.")
                    
            ghost_net.export_to_json()
            input("\nPressione Enter para continuar...")

        elif opcao == "res":
            for node_id in ghost_net.nodes:
                node = ghost_net.nodes[node_id]
                node.status = "normal"
                node.stability_timer = -1
            ghost_net.clear_highlights()
            incident.add_log("SISTEMA: Restauração total da rede executada.", "log_info")
            print("\n[!] Comando Fantasma: Todos os distritos estão ONLINE.")
            ghost_net.export_to_json()
            input("Pressione Enter para continuar...")

        elif opcao == "0":

            break
        
        elif opcao == "0":
            break
        
        ghost_net.export_to_json()  
        incident.process_turn(ghost_net)