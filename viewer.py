import pygame
import sys
import json

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GhostNet - Monitoramento")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 14, bold=True)

BG_COLOR = (15, 15, 20)
EDGE_COLOR = (100, 100, 120)
HIGHLIGHT_EDGE = (0, 255, 255)
HIGHLIGHT_NODE = (255, 0, 255)
COLOR_NORMAL = (46, 204, 113)
COLOR_ALERTA = (241, 196, 15)
COLOR_OFFLINE = (231, 76, 60)

def load_network_data(previous_data):
    try:
        with open("cidade.json", "r") as f:
            return json.load(f)
    except Exception:
        return previous_data

def get_node_color(status):
    if status == "normal": return COLOR_NORMAL
    if status == "alerta": return COLOR_ALERTA
    if status == "offline": return COLOR_OFFLINE
    return (255, 255, 255)

running = True
data = {"nodes": {}, "edges": [], "highlighted_nodes": [], "highlighted_edges": []}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    data = load_network_data(data)

    screen.fill(BG_COLOR)

    high_edges = data.get("highlighted_edges", [])
    high_nodes = data.get("highlighted_nodes", [])

    for edge in data["edges"]:
        n1 = edge["source"]
        n2 = edge["target"]
        if n1 in data["nodes"] and n2 in data["nodes"]:
            x1, y1 = data["nodes"][n1]["x"], data["nodes"][n1]["y"]
            x2, y2 = data["nodes"][n2]["x"], data["nodes"][n2]["y"]
            
            color = HIGHLIGHT_EDGE if [n1, n2] in high_edges or [n2, n1] in high_edges else EDGE_COLOR
            thickness = 5 if color == HIGHLIGHT_EDGE else 2
            
            pygame.draw.line(screen, color, (x1, y1), (x2, y2), thickness)

    for node_id, info in data["nodes"].items():
        x, y = info["x"], info["y"]
        color = get_node_color(info["status"])
        
        if node_id in high_nodes:
            pygame.draw.circle(screen, HIGHLIGHT_NODE, (x, y), 26, 3)
            
        pygame.draw.circle(screen, color, (x, y), 20)
        
        text_surf = font.render(node_id, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(x, y - 30))
        screen.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()