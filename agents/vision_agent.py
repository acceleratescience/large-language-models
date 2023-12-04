import openai
from openai import OpenAI
import json
import requests
import base64

from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()


class VisionAgent:
    """
    A vision agent that uses OpenAI's API to generate a response to an image.
    """
    def __init__(self, model : str = "gpt-4-vision-preview"):
        self.client = OpenAI()
        self.model = model
        

    def get_response(self, prompt : str, image_path : str) -> dict:
        """_summary_

        Args:
            image (str): _description_
            image_name (str): _description_
            dump (bool, optional): _description_. Defaults to True.

        Returns:
            dict: _description_
        """
        base64_image = self._encode_image(image_path)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
            {
                "role": "user",
                "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:image/png;base64,{base64_image}",
                    },
                },
                ],
            }
            ],
            max_tokens=256,
        )
        return response.choices[0].message.content

        
    def _encode_image(self, image_path):
        """_summary_

        Args:
            image_path (_type_): _description_

        Returns:
            _type_: _description_
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
