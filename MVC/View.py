from pygame import gfxdraw
import pygame
from pygame import *
from MVC import Model, Controller
from client import Client


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # class View:


Controller.parse_graph()
graph = Controller.get_graph()
client = Client()
pygame.init()
# init pygame
WIDTH, HEIGHT = 1080, 720
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)
radius = 15

# decorate scale with the correct values

# get data proportions
min_x = min(list(graph.nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.nodes), key=lambda n: n.pos.y).pos.y


def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


while client.is_running() == 'true':

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph.nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # It's just to get a nice antialiasing circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    # pokemons = [p.Pokemon for p in pokemons]
    # for p in pokemons:
    #     x, y, _ = p.pos.split(',')
    #     p.pos = SimpleNamespace(x=my_scale(
    #         float(x), x=True), y=my_scale(float(y), y=True))
    # agents = json.loads(client.get_agents(),
    #                     object_hook=lambda d: SimpleNamespace(**d)).Agents
    # agents = [agent.Agent for agent in agents]
    # for a in agents:
    #     x, y, _ = a.pos.split(',')
    #     a.pos = SimpleNamespace(x=my_scale(
    #         float(x), x=True), y=my_scale(float(y), y=True))

    # parsing pokemons and agents
    Controller.parse_pokemon()
    Controller.parse_agents()
    pokemons = Controller.get_pokemons()
    agents = Controller.get_agents()

    # draw agents- p
    # for agent in agents:
    #     pygame.draw.circle(screen, Color(122, 61, 23),
    #                        (int(agent.pos.x), int(agent.pos.y)), 10)



    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)
