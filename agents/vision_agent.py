import openai
from openai import OpenAI
import json
import requests
import base64

from dotenv import load_dotenv
import os
load_dotenv()


class VisionAgent:
    """
    A vision agent that uses OpenAI's API to generate a response to an image.
    """
    def __init__(self, mode : str = "normal", model : str = "gpt-4-vision-preview"):
        self.mode = mode
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.prompt = self._get_system_prompt()
        

    def get_response(self, image : str, image_name : str, dump : bool = True) -> dict:
        """_summary_

        Args:
            image (str): _description_
            image_name (str): _description_
            dump (bool, optional): _description_. Defaults to True.

        Returns:
            dict: _description_
        """
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": self.prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:image/png;base64,{self._encode_image(image)}"
                    }
                }
                ]
            }
            ],
            "max_tokens": 300
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)

        if dump:
            with open(f'responses/{self.mode}/{image_name}_response.json', 'w') as file:
                json.dump(response.json(), file, indent=4)

        return response.json()


    def _get_system_prompt(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        with open(f'prompts/{self.mode}_prompt.txt', 'r') as file:
            prompt = file.read()
        
        return prompt
        

    def _encode_image(self, image_path):
        """_summary_

        Args:
            image_path (_type_): _description_

        Returns:
            _type_: _description_
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
