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
    print("1. Simular Falha | 2. Restaurar | 3. Conectividade (BFS) | 4. Buscar nos Logs (Rabin-Karp) | 0. Sair")

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
            search_term = input("\nTermo de busca nos logs: ")
            print(f"\n--- RESULTADOS PARA: '{search_term}' ---")
            found = False
            for log in incident.event_logs:
                # Removemos os códigos de cores ANSI para a busca não falhar
                clean_log = log.replace("\033[91m", "").replace("\033[93m", "").replace("\033[94m", "").replace("\033[0m", "")
                
                if algorithms.rabin_karp(clean_log.lower(), search_term.lower()):
                    print(log)
                    found = True
            
            if not found:
                print("Nenhum registro encontrado.")
            input("\nPressione Enter para continuar...")    

        elif opcao == "0":
            break
        
        incident.process_turn(ghost_net)