import tcod as libtcod
import tcod.event

def handle_keys(key_event):
    # Movement keys
    if key_event.sym == tcod.event.K_UP:
        return {'move': (0, -1)}
    elif key_event.sym == tcod.event.K_DOWN:
        return {'move': (0, 1)}
    elif key_event.sym == tcod.event.K_LEFT:
        return {'move': (-1, 0)}
    elif key_event.sym == tcod.event.K_RIGHT:
        return {'move': (1, 0)}

    if key_event.sym == tcod.event.K_RETURN and key_event.mod == tcod.event.KMOD_LALT:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key_event.sym == tcod.event.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key_event was pressed
    return {}
