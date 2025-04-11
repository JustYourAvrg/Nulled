from helpers.helpers import HelperFunctions


class DetectBiome:
    def __init__(self):
        self.helper = HelperFunctions()


    def DetectBiome(self, biomes):
        log_data = list(reversed(self.helper.log_file_data()))[:500]

        for line in log_data:
            for biome in biomes:
                if biome in line:
                    return biome

        return None