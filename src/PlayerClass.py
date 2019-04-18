
import tcod as libtcod

from DrawOrderClass import BasicDrawOrder, BarDrawOrder, TextDrawOrder

class PlayerObject(object):
    def __init__(self, name="The Reaper"):
        self.coordX = 0
        self.coordY = 0

        self.icon = "@"
        self.name = name

        self.hp = 20
        self.maxHP = self.hp
        
        self.stam = 20
        self.maxStam = self.stam

        self.magic = 20
        self.maxMagic = self.magic

        self.level = 1
        self.xp = 0
        self.xpToNextLevel = 20

        self.backlog = []

    def getDrawOrders(self, map_console, hud_console, quest_console, hud_width=30):
        drawOrders = []
        drawOrders.append(BasicDrawOrder(map_console, self.icon, libtcod.white, self.coordX, self.coordY))
        drawOrders.append(self.getTitleDrawOrder(hud_console, hud_width))
        drawOrders.append(
            self.getExperienceBarDrawOrder(hud_console, hud_width))
        drawOrders.append(self.getHealthBarDrawOrder(hud_console, hud_width))
        drawOrders.append(self.getStaminaBarDrawOrder(hud_console, hud_width))
        drawOrders.append(self.getMagicBarDrawOrder(hud_console, hud_width))
        return drawOrders
    
    def getTitleDrawOrder(self, hud_console, hud_width):
        drawOrder = TextDrawOrder(hud_console, "{} - Level {}".format(self.name, self.level), int(hud_width/2), 0, "center")
        return drawOrder
    
    def getExperienceBarDrawOrder(self, hud_console, hud_width):
        barwidth = int(float(self.xp) / self.xpToNextLevel * hud_width)
        return BarDrawOrder(hud_console, "Experience ({}/{})".format(self.xp, self.xpToNextLevel), barwidth, libtcod.azure, 0, 1)

    def getHealthBarDrawOrder(self, hud_console, hud_width):
        barwidth = int(float(self.hp) / self.maxHP * hud_width)
        return BarDrawOrder(hud_console, "Health ({}/{})".format(self.hp, self.maxHP), barwidth, libtcod.darker_red, 0, 2)
    
    def getStaminaBarDrawOrder(self, hud_console, hud_width):
        barwidth = int(float(self.stam) / self.maxStam * hud_width)
        return BarDrawOrder(hud_console, "Stamina ({}/{})".format(self.stam, self.maxStam), barwidth, libtcod.darker_green, 0, 3)

    def getMagicBarDrawOrder(self, hud_console, hud_width):
        barwidth = int(float(self.magic) / self.maxMagic * hud_width)
        return BarDrawOrder(hud_console, "Magic ({}/{})".format(self.magic, self.maxMagic), barwidth, libtcod.darker_blue, 0, 4)
    
    def getBacklog(self):
        backlog = self.backlog
        self.backlog = []
        return backlog

    def getX(self):
        return self.coordX
    
    def getY(self):
        return self.coordY
    
    def moveY(self, direction=0, walkable=True):
        if self.coordY + direction > 0 and walkable:
            self.coordY += direction
        else:
            self.backlog.append(("toast","Unable to move in that direction."))

    def moveX(self, direction=0, walkable=True):
        if self.coordX + direction > 0 and walkable:
            self.coordX += direction
        else:
            self.backlog.append(("toast","Unable to move in that direction."))