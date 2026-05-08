class Node:
    def __init__(self, node_id, node_type="Data"):
        self.id = node_id
        self.type = node_type
        self.status = "normal"
        self.stability_timer = -1

class Network:
    def __init__(self):
        self.nodes = {}
        self.adj_list = {}

    def add_node(self, node_id, node_type="Data"):
        if node_id not in self.nodes:
            new_node = Node(node_id, node_type)
            self.nodes[node_id] = new_node
            self.adj_list[node_id] = []

    def add_connection(self, origin, destination, weight=1):
        if origin in self.nodes and destination in self.nodes:
            self.adj_list[origin].append((destination, weight))
            self.adj_list[destination].append((origin, weight))