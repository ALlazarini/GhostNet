from collections import deque

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

def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)
    if m > n: return False
    
    prime = 101
    base = 256
    h_pattern = 0
    h_text = 0
    h_multiplier = 1

    for i in range(m - 1):

        h_multiplier = (h_multiplier * base) % prime

    for i in range(m):

        h_pattern = (base * h_pattern + ord(pattern[i])) % prime
        h_text = (base * h_text + ord(text[i])) % prime

    for i in range(n - m + 1):

        if h_pattern == h_text:

            if text[i:i+m] == pattern:

                return True
        
        if i < n - m:

            h_text = (base * (h_text - ord(text[i]) * h_multiplier) + ord(text[i+m])) % prime

            if h_text < 0:

                h_text += prime
                
    return False

