
from jsonDecoder import loadJson


class DatapackObject(object):
    def __init__(self, loaded_meta_data, datapack_folder):
        self.metadata = loaded_meta_data
        self.folder = datapack_folder
        self.regions = {}
        self.procs = {}

        # Not currently implemented
        self.enemies = {}
        self.items = {}
    
    def loadAllDataFiles(self):
        print("Loading Datapack...")
        print("\tLoading Regions...")
        for region in self.metadata["Regions"]:
            print("\t\t{}".format(region))
            regionFolder = self.metadata["RegionFolder"]
            loadString = "{}{}{}.json".format(
                self.folder, regionFolder, region)
            self.regions[region] = loadJson(loadString)
        print("\tLoading Procs...")
        for proc in self.metadata["Procs"]:
            print("\t\t{}".format(region))
            procFolder = self.metadata["ProcFolder"]
            loadString = "{}{}{}.json".format(
                self.folder, procFolder, proc)
            self.procs[proc] = loadJson(loadString)
        print("Finished loading datapack files.")
    
    def getRegionData(self, region):
        return self.regions[region]
