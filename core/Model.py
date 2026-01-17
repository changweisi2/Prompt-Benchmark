# -*- coding: utf-8 -*-
import json

import requests
import base64

import time

from random import choice
from typing import List


class Model:
    def __init__(self, api_key, base_url, model_name, temperature):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = api_key
        self.url = base_url

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def execute(self, full_prompt):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }



        while True:
            try:
                data = {
                    "model": f"{self.model_name}",  # model参数
                    "temperature": self.temperature,
                    "messages": [
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ]
                }

                response = requests.post(self.url, headers=headers, data=json.dumps(data), verify=True)

                break

            except Exception as e:
                print('Exception:', e)
                time.sleep(1)
                continue

        return response

    def postprocess(self, response):
        """
        """
        model_output = None

        if isinstance(response, str):
            model_output = response
        else:
            model_output = response.choices[0].message.content
        return model_output




