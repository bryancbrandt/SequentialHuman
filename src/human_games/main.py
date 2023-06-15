import typing
import pygame as pg
from pygame.locals import *
import locals
from explosion import Explosion
from tank import Tank
from player import Player


def reveal_tank(tanklist: typing.List[Tank], player: Player) -> None:
    for tank in tanklist:
        if player.fog_of_war(tank):
            tank.revealed = True
    coord = str(player.rect.top) + "," + str(player.rect.left)
    print(f"State: {locals.coord_to_state[coord]}")


def main():
    FOG_OF_WAR = True
    pg.init()
    screen = pg.display.set_mode((1200, 600), pg.SCALED)  # 10 X 40
    pg.display.set_caption("Explosion Test")
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    clock = pg.time.Clock()

    # Game Groups
    tanks = pg.sprite.Group()
    all = pg.sprite.RenderUpdates()

    # Assign groups to sprite classes
    Explosion.containers = all, tanks
    Tank.containers = all
    Player.containers = all
    tank_list = []

    for i in range(10):
        tank_list.append(Tank(i * 30, i * 30))
    player = Player(300, 300)

    while True:
        clock.tick(40)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    player.moveright()
                    if FOG_OF_WAR:
                        reveal_tank(tank_list, player)

                if event.key == K_UP:
                    player.moveup()
                    if FOG_OF_WAR:
                        reveal_tank(tank_list, player)

                if event.key == K_LEFT:
                    player.moveleft()
                    if FOG_OF_WAR:
                        reveal_tank(tank_list, player)

                if event.key == K_DOWN:
                    player.movedown()
                    if FOG_OF_WAR:
                        reveal_tank(tank_list, player)

                if event.key == K_SPACE:
                    for tank in tank_list:
                        if player.fire(tank):
                            Explosion(tank)
                            tank.kill()
                            tank_list.remove(tank)

        all.update()
        screen.blit(background, (0, 0))
        dirty = all.draw(screen)
        pg.display.update(dirty)
        pg.display.flip()


if __name__ == "__main__":
    main()
