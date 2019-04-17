
from jsonDecoder import loadJson

class SettingsObject(object):
    def __init__(self, fileLoc, loadResFolder=True):
        print("Loading settings from {}".format(fileLoc))
        self.parsed = loadJson(fileLoc)
        if loadResFolder:
            self.resourceFolder = self.parsed["ResourceFolder"]
    
    def getSetting(self, setting):
        value = self.parsed[setting]
        return value
    
    def getResource(self, setting):
        resource = "{}{}".format(self.resourceFolder, self.parsed[setting])
        return resource

