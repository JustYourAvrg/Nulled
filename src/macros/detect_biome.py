from helpers.helpers import HelperFunctions


class DetectBiome:
    def __init__(self):
        self.helper = HelperFunctions()


    def DetectBiome(self, biomes):
        log_data = self.helper.log_file_data()

        for line in reversed(log_data):
            for biome in biomes:
                if biome in line:
                    return biome