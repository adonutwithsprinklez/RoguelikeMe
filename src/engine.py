
import tcod as libtcod

import tcod as libtcod

from DisplayClass import DisplayObject
from GameClass import GameObject
from KeyHandler import processKeyPress
from SettingsClass import SettingsObject


#
# Main function
#
# This is the function that creates the game object, loads the settings,
# and runs the games main loop
def main():
    SETTINGS = SettingsObject("res/settings.json")

    # Start setting up the screens/panels
    # Sets the window dimensions
    window_width = SETTINGS.getSetting("WindowWidth")
    window_height = SETTINGS.getSetting("WindowHeight")
    screen_names = SETTINGS.getSetting("Screens")
    
    # Initiate the Display
    display = DisplayObject()

    # Puts all screen settings into a dictionary
    for screen_name in screen_names:
        screen_data = SETTINGS.getSetting(screen_name)
        display.panelInfo[screen_name] = screen_data

    # Create the displays:
    map_console = libtcod.console_new(
        display.panelInfo["MapScreen"]["ScreenWidth"], display.panelInfo["MapScreen"]["ScreenHeight"])
    hud_console = libtcod.console_new(
        display.panelInfo["HUDScreen"]["ScreenWidth"], display.panelInfo["HUDScreen"]["ScreenHeight"])
    quest_console = libtcod.console_new(
        display.panelInfo["QuestScreen"]["ScreenWidth"], display.panelInfo["QuestScreen"]["ScreenHeight"])
    toast_console = libtcod.console_new(
        display.panelInfo["ToastScreen"]["ScreenWidth"], display.panelInfo["ToastScreen"]["ScreenHeight"])

    # Set the font
    libtcod.console_set_custom_font(SETTINGS.getResource("FontFile"),
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Initialize display
    libtcod.console_init_root(
        window_width, window_height, 'Roguelike Me', False)

    # Create the game object:
    Game = GameObject(SETTINGS)


    #
    # MAIN LOOP
    #
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    while not libtcod.console_is_window_closed():
        
        # Turn key press into an action, otherwise return None
        action = processKeyPress(key)
        
        # Process action if not None
        if action != None:
            if action[0] == 'fullscreen':
                libtcod.console_set_fullscreen(
                    not libtcod.console_is_fullscreen())
            elif action[0] == 'quit'and action[1] == True:
                return True
            else:
                # If the action is meant for the game itself instead of the program,
                # send it forward to the game to update later
                Game.addActionToBacklog(action)
            # Process backlog after keypress if the action did something.
            Game.processBacklog()

        # Get all draw updates from the Game
        toDraw = Game.getToDraw(map_console, hud_console, quest_console, toast_console)

        # Forward all draw updates to the display
        display.setDrawOrders(toDraw)

        # Print to Panels
        display.drawToPanels(True)
        display.renderPanels(map_console, hud_console,
                             quest_console, toast_console)

        # Wait for Keypress
        libtcod.sys_wait_for_event(
            libtcod.EVENT_KEY_PRESS, key, mouse, True)


if __name__ == '__main__':
    main()
