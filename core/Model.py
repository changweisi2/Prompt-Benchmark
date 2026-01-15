# -*- coding: utf-8 -*-
import json

import requests
import base64

import time
import openai
from random import choice
from typing import List


class Model:
    def __init__(self, api_key, base_url, model_name, temperature, max_tokens):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key
        self.url = base_url

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def execute(self, prompt, question, pictures):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        user_content = question
        picture_urls = [
            "以下是图片路径"
        ]
        for pict in pictures:
            picture_urls.append(
                f"image_url:data:image/png;base64,{self.encode_image(pict)}"
            )

        user_content += "\n".join(picture_urls)

        while True:
            try:
                data = {
                    "model": f"{self.model_name}",  # model参数
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "messages": [
                        {
                            "role": "system",
                            "content": prompt
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                }

                response = requests.post(self.url, headers=headers, data=json.dumps(data), verify=False)

                break
            except openai.BadRequestError as e:
                print('BadRequestError:', e)
                response = "Your input image may contain content that is not allowed by our safety system."
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




