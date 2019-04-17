
import tcod as libtcod


class DisplayObject(object):
    def __init__(self):
        self.panelInfo = {}
        self.drawOrders = []

    def addDrawOrder(self, drawOrder):
        self.drawOrders.append(drawOrder)

    def setDrawOrders(self, drawOrders=[]):
        self.drawOrders = drawOrders

    def drawToPanels(self, clearOrders=True):
        # Draw the orders to the panels
        for draw_order in self.drawOrders:
            drawInfo = draw_order.getDrawInfo()
            if drawInfo[0] == "basic":
                self.drawChar(drawInfo[1:])
            elif drawInfo[0] == "bar":
                self.drawBar(drawInfo[1:])
            elif drawInfo[0] == "print":
                self.drawText(drawInfo[1:])
        if clearOrders:
            self.drawOrders = []

    def drawChar(self, drawInfo):
        libtcod.console_put_char(drawInfo[0], drawInfo[1], drawInfo[2],
                                 drawInfo[3], libtcod.BKGND_NONE)
    
    def drawText(self, drawInfo):
        if drawInfo[4] == "left":
            alignment = libtcod.LEFT
        elif drawInfo[4] == "right":
            alignment = libtcod.RIGHT
        elif drawInfo[4] == "center":
            alignment = libtcod.CENTER
        libtcod.console_print_ex(
            drawInfo[0], drawInfo[2], drawInfo[3], libtcod.BKGND_NONE, alignment, drawInfo[1])

    def drawBar(self, drawInfo):
        title = " " + drawInfo[1]
        libtcod.console_print_ex(drawInfo[0], drawInfo[4], drawInfo[5], libtcod.BKGND_NONE, libtcod.LEFT, title)
        libtcod.console_set_default_background(drawInfo[0], drawInfo[3])
        if drawInfo[2] > 0:
            libtcod.console_rect(drawInfo[0], drawInfo[4], drawInfo[5], drawInfo[2], 1, False, libtcod.BKGND_SCREEN)
        libtcod.console_set_default_background(drawInfo[0], libtcod.black)

    def renderPanels(self, map_console, hud_console, quest_console, toast_console):
        # Draw the panels to the console
        libtcod.console_blit(
            map_console, 0, 0, self.panelInfo["MapScreen"][
                "ScreenWidth"], self.panelInfo["MapScreen"]["ScreenHeight"],
            0, self.panelInfo["MapScreen"]["StartX"], self.panelInfo["MapScreen"]["StartY"])
        libtcod.console_blit(
            hud_console, 0, 0, self.panelInfo["HUDScreen"][
                "ScreenWidth"], self.panelInfo["HUDScreen"]["ScreenHeight"],
            0, self.panelInfo["HUDScreen"]["StartX"], self.panelInfo["HUDScreen"]["StartY"])
        libtcod.console_blit(
            quest_console, 0, 0, self.panelInfo["QuestScreen"][
                "ScreenWidth"], self.panelInfo["QuestScreen"]["ScreenHeight"],
            0, self.panelInfo["QuestScreen"]["StartX"], self.panelInfo["QuestScreen"]["StartY"])
        libtcod.console_blit(
            toast_console, 0, 0, self.panelInfo["ToastScreen"][
                "ScreenWidth"], self.panelInfo["ToastScreen"]["ScreenHeight"],
            0, self.panelInfo["ToastScreen"]["StartX"], self.panelInfo["ToastScreen"]["StartY"])

        # Update Panels
        libtcod.console_flush()

        # Clear Panels
        libtcod.console_clear(map_console)
        libtcod.console_clear(hud_console)
        libtcod.console_clear(quest_console)
        libtcod.console_clear(toast_console)
