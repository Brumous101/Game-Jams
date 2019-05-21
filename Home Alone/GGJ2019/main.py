import map
import npc
import player
import pygame

win_width = 800
win_height =600
display = pygame.display.set_mode((800,600))

clock = pygame.time.Clock()

house = map.Map("maps\\firstmap.txt", (1048, 0), (0, 0), (0, 0), (0, 0), clock)
char = player.Player((20, 10),house.get_tile_dimensions())
npc = npc.npc_create("npc.txt")
house.addPlayer(char)
for i in npc:
    char.mMap.addnpc(i)





while True:
    pygame.display.flip()
    evt = pygame.event.poll()
    dt = clock.tick(60) / 1000.0
    if evt.type == pygame.QUIT:
        done = True
    elif evt.type == pygame.KEYDOWN:
        if evt.key == pygame.K_ESCAPE:
            done = True
            break

    keys = pygame.key.get_pressed()
    char.handle_keys(keys, dt)
    house.setCamera((char.mPos[0] - win_width // 2, char.mPos[1] - win_height // 2), (win_width, win_height))

    display.fill((0, 0, 0))
    house.draw(display)
    char.render(display, dt)

    for i in npc:
        i.draw(display,dt)
        if(i.check_vision(char.mPos)):
            print("hit")