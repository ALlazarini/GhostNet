import time
import random

COLORS = {
    "normal": "\033[0m",
    "alerta": "\033[93m",
    "offline": "\033[91m",
    "log_info": "\033[94m",
    "reset": "\033[0m"
}

event_logs = []

def add_log(message, level="normal"):
    timestamp = time.strftime("%H:%M:%S")
    color = COLORS.get(level, COLORS["reset"])
    event_logs.append(f"{color}[{timestamp}] {message}{COLORS['reset']}")
    if len(event_logs) > 5:
        event_logs.pop(0)

def apply_incident(network, node_id):
    if node_id in network.nodes:
        node = network.nodes[node_id]
        node.status = "offline"
        node.stability_timer = -1
        add_log(f"CRÍTICO: {node_id} está OFFLINE!", "offline")
        
        # Dependências Fixas
        if node_id == "hub-01":
            for fixed in ["stor-01", "back-01"]:
                trigger_alert(network, fixed, 2)
        elif node_id == "stor-01":
            trigger_alert(network, "hub-01", 1)
        elif node_id == "back-01":
            trigger_alert(network, "stor-01", 1)
        
        # Dependência por Proximidade (Vizinhos)
        for neighbor, _ in network.adj_list[node_id]:
            if network.nodes[neighbor].status == "normal":
                trigger_alert(network, neighbor, 3)

def trigger_alert(network, node_id, turns):
    node = network.nodes[node_id]
    if node.status != "offline":
        node.status = "alerta"
        node.stability_timer = turns
        add_log(f"AVISO: {node_id} em alerta ({turns}T)", "alerta")

def process_turn(network):
    for node_id, node in network.nodes.items():
        if node.status == "alerta" and node.stability_timer > 0:
            node.stability_timer -= 1
            if node.stability_timer == 0:
                apply_incident(network, node_id)