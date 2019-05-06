
from RegionClass import RegionObject


class MapObject(object):
    def __init__(self, datapackHolder, width=40, height=40):
        self.datapackHolder = datapackHolder
        self.datapackHolder.loadAllDataFiles()
        
        self.width = width
        self.height = height

        self.currentRegion = None
    
    def generateRegion(self, region_x=0, region_y=0):
        test_region_data = self.datapackHolder.getRegionData("test_region")
        self.currentRegion = RegionObject(test_region_data, self.width, self.height)

        neededProcs = self.currentRegion.getProcFiles()
        procsToPass = self.datapackHolder.getProcs(neededProcs)
        self.currentRegion.loadProcs(procsToPass)
        
        neededTiles = self.currentRegion.getUnloadedTiles()
        tilesToPass = self.datapackHolder.getTiles(neededTiles)
        self.currentRegion.loadTiles(tilesToPass)
        
        self.currentRegion.generateWorld()
    
    def getDrawOrders(self, map_console):
        toDraw = []
        for drawOrder in self.currentRegion.getDrawOrders(map_console):
            toDraw.append(drawOrder)
        return toDraw
    
    def getWalkable(self, player_x=0, player_y=0):
        return self.currentRegion.getWalkable(player_x, player_y)
