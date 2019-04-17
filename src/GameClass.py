
from MapClass import MapObject
from PlayerClass import PlayerObject
from SettingsClass import SettingsObject

class GameObject(object):
    def __init__(self, settings):

        self.settings = settings

        # Get data pack info
        resFolder = self.settings.getSetting("ResourceFolder")
        dataPackFolder = self.settings.getSetting("DefaultDataPack")
        dataPackMetaFile = "{}{}/meta.json".format(resFolder, dataPackFolder)
        self.dataPackInfo = SettingsObject(dataPackMetaFile, False)

        self.mapSettings = settings.getSetting("MapScreen")
        self.mapWidth = self.mapSettings["ScreenWidth"]
        self.mapHeight = self.mapSettings["ScreenWidth"]

        self.hudSettings = settings.getSetting("HUDScreen")
        self.hudWidth = self.hudSettings["ScreenWidth"]
        self.hudHeight = self.hudSettings["ScreenWidth"]

        # Create the player
        self.player = PlayerObject()
        self.player.coordX = int(self.mapWidth/2)-1
        self.player.coordY = int(self.mapHeight/2)-1

        self.toDraw = []
        self.backlog = []

    def getToDraw(self, mapConsole, hud_console, quest_console, toast_console):
        for drawOrder in self.player.getDrawOrders(mapConsole, hud_console, quest_console, self.hudWidth):
            self.toDraw.append(drawOrder)

        toDraw = self.toDraw
        self.toDraw = []
        return toDraw
    
    def addActionToBacklog(self, action):
        self.backlog.append(action)

    def processBacklog(self, clearBacklog = True):
        for action in self.backlog:
            if action[0] == "movePlayer":
                if action[1] == 0 and self.player.getY() > 0:
                    self.player.coordY -= 1
                elif action[1] == 1 and self.player.getX() < self.mapWidth-1:
                    self.player.coordX += 1
                elif action[1] == 2 and self.player.getY() < self.mapHeight-1:
                    self.player.coordY += 1
                elif action[1] == 3 and self.player.getX() > 0:
                    self.player.coordX -= 1
        
        if clearBacklog:
            self.backlog = []
