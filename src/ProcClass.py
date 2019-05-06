
from TileClass import Tile

class ProcObject(object):
    def __init__(self, proc_data):
        self.data = proc_data
        self.name = self.data["Name"]
        self.procID = self.data["ProcID"]
        self.unloadedTiles = self.data["Tiles"]

        self.variations = self.data["Variations"]

        self.tiles = {}


    def loadTiles(self, neededTiles=[]):
        for tiledata in neededTiles:
            self.loadTile(tiledata)

        for tiledata in self.data["CustomTiles"]:
            self.loadTile(tiledata,True)
    
    def loadTile(self, tiledata, addProcID = False):
        tileID = tiledata["tileid"]
        if addProcID:
            tileID = "{}-{}".format(self.procID, tileID)
        tileIcon = tiledata["icon"]
        tileWalkable = tiledata["walkable"]
        tilePassable = tiledata["viewable"]
        tileColor = tiledata["color"]
        self.tiles[tileID] = Tile(
            tileIcon, tilePassable, tileWalkable, tileColor)
        
    def getUnloadedTiles(self):
        return self.unloadedTiles
    
    def getCustomTiles(self):
        return self.tiles
