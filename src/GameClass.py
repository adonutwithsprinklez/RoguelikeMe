
from jsonDecoder import loadJson
from MapClass import RegionObject
from PlayerClass import PlayerObject
from SettingsClass import SettingsObject

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

        # Get data pack info
        resFolder = self.settings.getSetting("ResourceFolder")
        dataPackFolder = self.settings.getSetting("DefaultDataPack")
        dataPackMetaFile = "{}{}/meta.json".format(resFolder, dataPackFolder)
        self.dataPackInfo = SettingsObject(dataPackMetaFile, False)

        # Create the gamemap
        regionFolder = self.dataPackInfo.getSetting("RegionFolder")
        test_region_name = self.dataPackInfo.getSetting("RegionStart")
        test_region_file = "{}{}/{}{}.json".format(resFolder, dataPackFolder, regionFolder, test_region_name)
        test_region_data = loadJson(test_region_file)
        self.currentRegion = RegionObject(test_region_data)
        self.currentRegion.generateWorld()

        # Create the player
        playername = self.settings.getSetting("DefaultPlayerName")
        self.player = PlayerObject(playername)
        self.player.coordX = int(self.mapWidth/2)-1
        self.player.coordY = int(self.mapHeight/2)-1

        self.toDraw = []
        self.backlog = []

    def getToDraw(self, mapConsole, hud_console, quest_console, toast_console):
        for drawOrder in self.currentRegion.getDrawOrders(mapConsole):
            self.toDraw.append(drawOrder)

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
                    walkable = self.currentRegion.getWalkable(self.player.getX(),self.player.getY()-1)
                    self.player.moveY(-1, walkable)
                elif action[1] == 1 and self.player.getX() < self.mapWidth-1:
                    walkable = self.currentRegion.getWalkable(self.player.getX()+1,self.player.getY())
                    self.player.moveX(1, walkable)
                elif action[1] == 2 and self.player.getY() < self.mapHeight-1:
                    walkable = self.currentRegion.getWalkable(self.player.getX(),self.player.getY()+1)
                    self.player.moveY(1, walkable)
                elif action[1] == 3 and self.player.getX() > 0:
                    walkable = self.currentRegion.getWalkable(self.player.getX()-1,self.player.getY())
                    self.player.moveX(-1, walkable)
        for action in self.player.getBacklog():
            if action[0] == "toast":
                print(action[1])
        
        if clearBacklog:
            self.backlog = []
