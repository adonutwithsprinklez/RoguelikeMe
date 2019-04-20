
from DatapackClass import DatapackObject
from jsonDecoder import loadJson
from MapClass import MapObject
from PlayerClass import PlayerObject
from SettingsClass import SettingsObject
from ToastClass import ToastObject

class GameObject(object):
    def __init__(self, settings):

        self.settings = settings

        # Get some display variables
        self.mapSettings = settings.getSetting("MapScreen")
        self.mapWidth = self.mapSettings["ScreenWidth"]
        self.mapHeight = self.mapSettings["ScreenWidth"]
        self.hudSettings = settings.getSetting("HUDScreen")
        self.hudWidth = self.hudSettings["ScreenWidth"]
        self.hudHeight = self.hudSettings["ScreenWidth"]
        self.toastSettings = settings.getSetting("ToastScreen")
        self.toastWidth = self.toastSettings["ScreenWidth"]
        self.toastHeight = self.toastSettings["ScreenHeight"]

        # Create the toasting object
        self.toaster = ToastObject(self.toastHeight, self.toastWidth)

        # Get data pack info
        resFolder = self.settings.getSetting("ResourceFolder")
        dataPackFolder = "{}{}/".format(
            resFolder, self.settings.getSetting("DefaultDataPack"))
        dataPackMetaFile = "{}meta.json".format(dataPackFolder)
        loadedDataPackMetaFile = loadJson(dataPackMetaFile)
        dataPackInfo = DatapackObject(loadedDataPackMetaFile, dataPackFolder)

        # Create the gamemap
        self.gameMap = MapObject(dataPackInfo, self.mapWidth, self.mapHeight)
        self.gameMap.generateRegion()

        # Create the player
        playername = self.settings.getSetting("DefaultPlayerName")
        self.player = PlayerObject(playername)
        self.player.coordX = int(self.mapWidth/2)-1
        self.player.coordY = int(self.mapHeight/2)-1

        self.toDraw = []
        self.backlog = []

        self.toaster.toast("Welcome to Roguelike Me")
        self.toaster.toast("This game is an obvious work in progress.")

    def getToDraw(self, mapConsole, hud_console, quest_console, toast_console):
        for drawOrder in self.gameMap.getDrawOrders(mapConsole):
            self.toDraw.append(drawOrder)

        for drawOrder in self.player.getDrawOrders(mapConsole, hud_console, quest_console, self.hudWidth):
            self.toDraw.append(drawOrder)

        for drawOrder in self.toaster.getDrawOrders(toast_console):
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
                    walkable = self.gameMap.getWalkable(
                        self.player.getX(), self.player.getY()-1)
                    self.player.moveY(-1, walkable)
                elif action[1] == 1 and self.player.getX() < self.mapWidth-1:
                    walkable = self.gameMap.getWalkable(
                        self.player.getX()+1, self.player.getY())
                    self.player.moveX(1, walkable)
                elif action[1] == 2 and self.player.getY() < self.mapHeight-1:
                    walkable = self.gameMap.getWalkable(
                        self.player.getX(), self.player.getY()+1)
                    self.player.moveY(1, walkable)
                elif action[1] == 3 and self.player.getX() > 0:
                    walkable = self.gameMap.getWalkable(
                        self.player.getX()-1, self.player.getY())
                    self.player.moveX(-1, walkable)
#            elif action[0] == "GameDebug":
#                self.toaster.toast("Player coords: ({},{})".format(
#                    self.player.getX(), self.player.getY()))
#                self.toaster.toast("This really long action that should be put onto 2 lines")
        for action in self.player.getBacklog():
            if action[0] == "toast":
                self.toaster.toast(action[1])
        if clearBacklog:
            self.backlog = []
