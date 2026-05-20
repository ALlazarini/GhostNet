from collections import deque
import heapq
from collections import Counter
import heapq

def bfs_reachability(network, start_node):
    if start_node not in network.nodes or network.nodes[start_node].status == "offline":
        return []

    visited = set()
    queue = deque([start_node])
    visited.add(start_node)

    while queue:
        current = queue.popleft()
        for neighbor, _ in network.adj_list[current]:
            if neighbor not in visited and network.nodes[neighbor].status != "offline":
                visited.add(neighbor)
                queue.append(neighbor)

    return list(visited)

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)
    if m > n: return False
    prime, base = 101, 256
    h_pattern, h_text, h_multiplier = 0, 0, 1
    for i in range(m - 1):
        h_multiplier = (h_multiplier * base) % prime
    for i in range(m):
        h_pattern = (base * h_pattern + ord(pattern[i])) % prime
        h_text = (base * h_text + ord(text[i])) % prime
    for i in range(n - m + 1):
        if h_pattern == h_text and text[i:i+m] == pattern:
            return True
        if i < n - m:
            h_text = (base * (h_text - ord(text[i]) * h_multiplier) + ord(text[i+m])) % prime
            if h_text < 0: h_text += prime
    return False

def huffman_compress(text):

    if not text: return "", None
    frequency = Counter(text)
    pq = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(pq)
    while len(pq) > 1:
        left, right = heapq.heappop(pq), heapq.heappop(pq)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left, merged.right = left, right
        heapq.heappush(pq, merged)
    root = pq[0]
    codes = {}
    def build_codes(node, current):
        if node:
            if node.char: codes[node.char] = current
            build_codes(node.left, current + "0")
            build_codes(node.right, current + "1")
    build_codes(root, "")
    return "".join(codes[char] for char in text), root

def dfs_islands(network):

    visited = set()
    islands = []

    for node_id in network.nodes:
        if node_id not in visited and network.nodes[node_id].status != "offline":
            island = []
            stack = [node_id]
            visited.add(node_id)
            
            while stack:
                current = stack.pop()
                island.append(current)
                
                for neighbor, _ in network.adj_list[current]:
                    if neighbor not in visited and network.nodes[neighbor].status != "offline":
                        visited.add(neighbor)
                        stack.append(neighbor)
                        
            islands.append(island)
            
    return islands

def dijkstra_shortest_path(network, start, end):
    if start not in network.nodes or end not in network.nodes:
        return None, float('inf')
    
    if network.nodes[start].status == "offline" or network.nodes[end].status == "offline":
        return None, float('inf')

    distances = {node: float('inf') for node in network.nodes}
    distances[start] = 0
    previous = {node: None for node in network.nodes}
    pq = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_dist > distances[current_node]:
            continue

        if current_node == end:
            break

        for neighbor, weight in network.adj_list[current_node]:
            if network.nodes[neighbor].status == "offline":
                continue
            
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    if distances[end] == float('inf'):
        return None, float('inf')

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    return path, distances[end]

def agm_prim(network, start_node):
    if start_node not in network.nodes or network.nodes[start_node].status == "offline":
        return [], 0
    
    mst_edges = []
    visited = set([start_node])
    edges = []
    total_cost = 0
    
    for neighbor, weight in network.adj_list[start_node]:
        if network.nodes[neighbor].status != "offline":
            heapq.heappush(edges, (weight, start_node, neighbor))
            
    while edges:
        weight, frm, to = heapq.heappop(edges)
        if to not in visited and network.nodes[to].status != "offline":
            visited.add(to)
            mst_edges.append((frm, to, weight))
            total_cost += weight
            for next_neighbor, next_weight in network.adj_list[to]:
                if next_neighbor not in visited and network.nodes[next_neighbor].status != "offline":
                    heapq.heappush(edges, (next_weight, to, next_neighbor))
                    
    return mst_edges, total_cost

def recovery_toposort(dependencies):
    in_degree = {u: 0 for u in dependencies}
    for u in dependencies:
        for v in dependencies[u]:
            if v not in in_degree:
                in_degree[v] = 0
            in_degree[v] += 1
    
    queue = deque([u for u in in_degree if in_degree[u] == 0])
    order = []
    
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in dependencies.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    if len(order) != len(in_degree):
        return []
    return order