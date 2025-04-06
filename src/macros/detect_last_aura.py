import re
import time

from helpers.helpers import HelperFunctions


class DetectAura:
    def __init__(self):
        self.helper = HelperFunctions()

    
    def detect_aura(self):
        log_data = list(reversed(self.helper.log_file_data()))[:500]

        for line in log_data:
            match = re.search(r'"state":"Equipped \\"(.*?)\\""', line)
            
            if match:
                aura = match.group(1)
                return aura

        return
        


