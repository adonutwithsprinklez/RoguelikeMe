
import tcod as libtcod

def processKeyPress(key):
    keyChar = chr(key.c)
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return ('fullscreen', True)

    elif key.vk == libtcod.KEY_ESCAPE:
        return ('quit',True)
    
    # Player Movement
    elif key.vk == libtcod.KEY_UP or keyChar == "w":
        return ('movePlayer', 0)
    elif key.vk == libtcod.KEY_RIGHT or keyChar == "d":
        return ('movePlayer', 1)
    elif key.vk == libtcod.KEY_DOWN or keyChar == "s":
        return ('movePlayer', 2)
    elif key.vk == libtcod.KEY_LEFT or keyChar == "a":
        return ('movePlayer', 3)
    
    # Game Debug key
#    elif keyChar == "p":
#        return ('GameDebug',True)

    # Not a proper key presses
    else:
        return None