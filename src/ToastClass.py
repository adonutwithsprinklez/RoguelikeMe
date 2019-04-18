
import textwrap

from DrawOrderClass import TextDrawOrder

class ToastObject(object):
    def __init__(self, max_toasts=1, max_width=20):
        self.toasts = []
        self.maxToasts = max_toasts
        self.maxWidth = max_width

    def toast(self, message="Toast Message", deleteOldToasts=True):
        for newToast in textwrap.wrap(message, self.maxWidth):
            self.toasts.append(newToast)
        if deleteOldToasts:
            while len(self.toasts) > self.maxToasts:
                del(self.toasts[0])
    
    def getToasts(self, getOnlyMaxToasts=True):
        toasts = self.toasts
        if getOnlyMaxToasts:
            while len(toasts) > self.maxToasts:
                del(toasts[0])
        return toasts
    
    def getDrawOrders(self, toast_console):
        drawOrders = []
        y = 0
        for toast in self.getToasts(True):
            newOrder = TextDrawOrder(toast_console, toast, 0, y, "left")
            drawOrders.append(newOrder)
            y += 1
        return drawOrders
