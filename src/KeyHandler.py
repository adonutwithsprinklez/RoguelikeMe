
import tcod as libtcod

def processKeyPress(key):
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return ('fullscreen', True)

    elif key.vk == libtcod.KEY_ESCAPE:
        return ('quit',True)
    
    # Player Movement
    elif key.vk == libtcod.KEY_UP:
        return ('movePlayer', 0)
    elif key.vk == libtcod.KEY_RIGHT:
        return ('movePlayer', 1)
    elif key.vk == libtcod.KEY_DOWN:
        return ('movePlayer', 2)
    elif key.vk == libtcod.KEY_LEFT:
        return ('movePlayer', 3)

    # Not a proper key presses
    else:
        return None