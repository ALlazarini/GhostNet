import json

class Node:
    def __init__(self, node_id, node_type="Data", x=0, y=0):
        self.id = node_id
        self.type = node_type
        self.status = "normal"
        self.stability_timer = -1
        self.x = x
        self.y = y

class Network:
    def __init__(self):
        self.nodes = {}
        self.adj_list = {}
        self.highlighted_nodes = []
        self.highlighted_edges = []

    def add_node(self, node_id, node_type="Data", x=0, y=0):
        if node_id not in self.nodes:
            new_node = Node(node_id, node_type, x, y)
            self.nodes[node_id] = new_node
            self.adj_list[node_id] = []

    def add_connection(self, origin, destination, weight=1):
        if origin in self.nodes and destination in self.nodes:
            self.adj_list[origin].append((destination, weight))
            self.adj_list[destination].append((origin, weight))

    def clear_highlights(self):
        self.highlighted_nodes = []
        self.highlighted_edges = []

    def export_to_json(self, filename="cidade.json"):
        data = {
            "nodes": {},
            "edges": [],
            "highlighted_nodes": self.highlighted_nodes,
            "highlighted_edges": self.highlighted_edges
        }
        
        for node_id, node in self.nodes.items():
            data["nodes"][node_id] = {
                "type": node.type,
                "status": node.status,
                "x": node.x,
                "y": node.y
            }
            
        for origin, neighbors in self.adj_list.items():
            for dest, weight in neighbors:
                edge = sorted([origin, dest])
                edge_dict = {"source": edge[0], "target": edge[1], "weight": weight}
                if edge_dict not in data["edges"]:
                    data["edges"].append(edge_dict)
                    
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)