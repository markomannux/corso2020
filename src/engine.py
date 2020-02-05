import tcod as libtcod
import tcod.event

from components.fighter import Fighter
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colors = {
        'light_wall': libtcod.Color(82, 53, 52),
        'light_ground': libtcod.Color(82, 81, 52),
        'dark_wall': libtcod.Color(39, 40, 57),
        'dark_ground': libtcod.Color(50, 54, 87)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, fighter=fighter_component)
    entities = [player]

    libtcod.console_set_custom_font(
            'resources/arial10x10.png',
            libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(
            screen_width,
            screen_height,
            'pyrogue',
            False,
            libtcod.RENDERER_SDL2,
            vsync=True)

    con = libtcod.console.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)
    
    game_state = GameStates.PLAYERS_TURN

    while True:

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(
                con,
                entities,
                game_map,
                fov_map,
                fov_recompute,
                screen_width,
                screen_height,
                colors)
        fov_recompute = False
        libtcod.console_flush()
        clear_all(con, entities, fov_map)


        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()
            elif event.type == "KEYDOWN":
                action = handle_keys(event)

                move = action.get('move')
                exit = action.get('exit')
                fullscreen = action.get('fullscreen')

                if move and game_state == GameStates.PLAYERS_TURN:
                    dx, dy = move
                    destination_x = player.x + dx
                    destination_y = player.y + dy
                    if not game_map.is_blocked(destination_x, destination_y):
                        target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                        if target:
                            print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                        else:
                            player.move(dx, dy)
                            fov_recompute = True

                        game_state = GameStates.ENEMY_TURN

                if exit:
                    return True

                if fullscreen:
                    libtcod.console_set_fullscreen(
                            not libtcod.console_is_fullscreen())

                if game_state == GameStates.ENEMY_TURN:
                    for entity in entities:
                        if entity.ai:
                            entity.ai.take_turn()

                    game_state = GameStates.PLAYERS_TURN


    # while not libtcod.console_is_window_closed():
    #    libtcod.console_set_default_foreground(0, libtcod.white)
    #    libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE)
    #    libtcod.console_flush()

    #    key = libtcod.console_check_for_keypress()

    #    if key.vk == libtcod.KEY_ESCAPE:
    #        return True

if __name__ == '__main__':
    main()
