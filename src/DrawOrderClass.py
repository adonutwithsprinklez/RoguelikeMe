
import tcod as libtcod


class DrawOrderBase(object):
    def __init__(self, console, draw_id="base"):
        self.console = console
        self.id = draw_id

    def getDrawInfo(self):
        return [self.id, self.console]


class BasicDrawOrder(DrawOrderBase):
    def __init__(self, draw_console, draw_icon=" ", color=libtcod.white, coord_x=0, coord_y=0):
        super().__init__(draw_console, "basic")
        self.icon = draw_icon
        if color:
            self.color = color
        else:
            self.color = libtcod.white
        self.coordX = coord_x
        self.coordY = coord_y

    def getDrawInfo(self):
        info = super().getDrawInfo()
        info.append(self.color)
        info.append(self.coordX)
        info.append(self.coordY)
        info.append(self.icon)
        return info


class BarDrawOrder(DrawOrderBase):
    def __init__(self, console, title="Title", bar_width=0, bar_color=libtcod.gray, coord_x=0, coord_y=0):
        super().__init__(console, "bar")
        self.title = title
        self.barWidth = bar_width
        self.barColor = bar_color
        self.coordX = coord_x
        self.coordY = coord_y

    def getDrawInfo(self):
        info = super().getDrawInfo()
        info.append(self.title)
        info.append(self.barWidth)
        info.append(self.barColor)
        info.append(self.coordX)
        info.append(self.coordY)
        return info

class TextDrawOrder(DrawOrderBase):
    def __init__(self, draw_console, text="", coord_x=0, coord_y=0, alignment="left"):
        super().__init__(draw_console, "print")
        self.text = text
        self.coordX = coord_x
        self.coordY = coord_y
        self.alignment = alignment
    
    def getDrawInfo(self):
        info = super().getDrawInfo()
        info.append(self.text)
        info.append(self.coordX)
        info.append(self.coordY)
        info.append(self.alignment)
        return info
