
import random

from DrawOrderClass import BasicDrawOrder
from ProcClass import ProcObject
from TileClass import Tile


class RegionObject(object):
    def __init__(self, region_data, width=40, height=40):
        self.data = region_data
        self.name = self.data["Name"]
        self.regionID = self.data["RegionID"]
        self.unloadedTiles = self.data["Tiles"]
        self.procfiles = self.data["Procs"]

        # Region dimensions
        self.width = width
        self.height = height
        self.chunk = []
        self.tiles = {}

        # Load generation instructions
        self.generationInstructions = []
        for instruction in self.data["Generation"]:
            instructID = instruction[0]
            if len(instruction) > 1:
                instructArgs = instruction[1:]
                newstep = (instructID, instructArgs)
            else:
                newstep = (instructID)
            self.generationInstructions.append(newstep)
        self.tempVariables = {}

    def loadTiles(self, neededTiles=[]):
        for tiledata in neededTiles:
            self.loadTile(tiledata)

        for tiledata in self.data["CustomTiles"]:
            self.loadTile(tiledata)
            
    
    def loadTile(self, tiledata):
        tileID = tiledata["tileid"]
        tileIcon = tiledata["icon"]
        tileWalkable = tiledata["walkable"]
        tilePassable = tiledata["viewable"]
        tileColor = tiledata["color"]
        self.tiles[tileID] = Tile(
            tileIcon, tilePassable, tileWalkable, tileColor)

    def generateWorld(self):
        self.chunk = []
        for x in range(0, self.width):
            column = []
            for y in range(0, self.height):
                column.append(None)
            self.chunk.append(column)

        for instruction in self.generationInstructions:
            command = instruction[0]
            args = instruction[1]

            if command == "fill_rect":
                self.fillRect(args)
            elif command == "place_random":
                self.placeRandom(args)
            elif command == "place_tile":
                self.placeTile(args)
            elif command == "set_variable":
                self.setVariable(args)
        # Clear temporary variables
        self.tempVariables = {}

    # Generation functions
    def setVariable(self, args):
        variableType = args[0]
        varName = args[1]
        if variableType == "str":
            varVal = args[2]
        elif variableType == "num":
            varVal = self.parseValue("int", args[2])
        elif variableType == "rand_num":
            minVal = args[2][0]
            maxVal = args[2][1]
            varVal = random.randint(minVal, maxVal)
        self.tempVariables[varName] = varVal

    def parseValue(self, varType="int", varValue="0"):
        parsedVal = None
        if varType == "int":
            if type(varValue) is int:
                parsedVal = varValue
            elif varValue == "maxW":
                parsedVal = self.width-1
            elif varValue == "maxH":
                parsedVal = self.height-1
            else:
                parts = varValue.split(";")
                parsedVal = 0
                for part in parts:
                    if part[0] == "$":
                        parsedVal += self.tempVariables[part]
                    elif part[0] == "+":
                        parsedVal += int(part[1:])
                    elif part[0] == "-":
                        parsedVal -= int(part[1:])
                    elif part[0] == "/":
                        parsedVal /= int(part[1:])
                        parsedVal = int(parsedVal)
                    elif part[0] == "*":
                        parsedVal *= int(part[1:])
                        parsedVal = int(parsedVal)
        return parsedVal

    def fillRect(self, args):
        filltiles = args[0]
        startx = self.parseValue("int", args[1])
        starty = self.parseValue("int", args[2])
        endx = self.parseValue("int", args[3])
        endy = self.parseValue("int", args[4])
        if startx == -1:
            startx = self.width-1
        if starty == -1:
            starty = self.height-1
        if endx == -1:
            endx = self.width
        if endy == -1:
            endy = self.height
        x = startx
        for column in self.chunk[startx:endx]:
            y = starty
            for tile in column[starty:endy]:
                self.chunk[x][y] = random.choice(filltiles)
                y += 1
            x += 1

    def placeRandom(self, args):
        filltiles = args[0]
        startx = self.parseValue("int", args[1])
        starty = self.parseValue("int", args[2])
        endx = self.parseValue("int", args[3])
        endy = self.parseValue("int", args[4])
        numToPlace = args[5]
        if startx == -1:
            startx = self.width-1
        if starty == -1:
            starty = self.height-1
        if endx == -1:
            endx = self.width-1
        if endy == -1:
            endy = self.height-1
        for i in range(0, numToPlace):
            x = random.randint(startx, endx)
            y = random.randint(starty, endy)
            self.chunk[x][y] = random.choice(filltiles)

    def placeTile(self, args):
        fillTiles = args[0]
        x = self.parseValue("int", args[1])
        y = self.parseValue("int", args[2])
        self.chunk[x][y] = random.choice(fillTiles)

    # Getter functions
    def getDrawOrders(self, map_console):
        drawOrders = []
        x = 0
        for column in self.chunk:
            y = 0
            for tile in column:
                if tile:
                    tileicon = self.tiles[tile].icon
                    tilecolor = self.tiles[tile].color
                else:
                    tileicon = " "
                    tilecolor = None
                newOrder = BasicDrawOrder(
                    map_console, tileicon, tilecolor, x, y)
                drawOrders.append(newOrder)
                y += 1
            x += 1
        return drawOrders

    def getWalkable(self, x=0, y=0):
        tile =  self.chunk[x][y] 
        if tile:
            walkable = self.tiles[tile].getWalkable()
        else:
            walkable = True
        return walkable

    def getProcs(self):
        return self.procfiles

    def getUnloadedTiles(self):
        return self.unloadedTiles
