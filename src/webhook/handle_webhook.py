import requests
import datetime

import os, sys, pathlib
sys.path.append(os.path.join(pathlib.Path(__file__).parents[2].resolve(), 'src'))
from helpers.helpers import HelperFunctions


class Webhook:
    def __init__(self):
        self.helpers = HelperFunctions()

    
    def send_embed(self, title: str=None, text: str=None, ping_type: str=None, color: str="0x1e1e1e"):
        self.config_data = self.helpers.load_config()

        self.webhook_url = self.config_data['webhook_url']
        self.private_server_link = self.config_data['private_server_link']
        
        embed = {
            "title": f"{title}",
            "color": int(color, 16),

            "thumbnail": {
                "url": "https://i.imgur.com/jyRZzLu.png" 
            },

            "description": text,

            "fields": [
                {
                    "name": f"Private Server",
                    "value": self.private_server_link,
                    "inline": False
                }
            ],
        }


        content = ""
        if ping_type == "everyone":
            content = f"@everyone"
        elif ping_type == "jester":
            content = f"<@{self.config_data['webhook']['jester_ping_id']}>"
        elif ping_type == "mari":
            content = f"<@{self.config_data['webhook']['mari_ping_id']}>"
        elif ping_type == "aura_found":
            content = f"<@{self.config_data['webhook']['aura_found_id']}>"
        
        payload = {
            "content": content,
            "embeds": [embed] if title or text else []
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(url=self.webhook_url, json=payload, headers=headers)

        print(payload["content"])
        return response.status_code, response.text