#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      sanid
#
# Created:     26/06/2025
# Copyright:   (c) sanid 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv




class Gemini:
    def __init__(self, model_name):
        load_dotenv()
        api_key = os.getenv("API_KEY")

        self.model_name = model_name
        self.api_key = api_key

        self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, input_text, thinking = False):
        """Generates a response using specified gemini model
        using whatever prompt you give"""
        self.response = self.client.models.generate_content(
            model = self.model_name,
            contents = input_text,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
            ),
        )

        return self.response.text

    def send_images_and_text(self, prompt, text, img_bytes):
        """Prepare text and images and then send them to gemini"""

        # change the prompt as necessary
        #prompt = "I want you to summarise all this information for me, and make me revision notes so i can quickly read through it - after that, make me 5 exam questions. Some information may be provided in images too so make to read and understand them too"
        contents = [prompt, text]

        for image_byte in img_bytes:
            contents.append(
                types.Part.from_bytes(
                    data=image_byte,
                    mime_type='image/jpeg'
                )
            )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget =  -1) # Gemini decides how much it needs to think
            ),
        )

        return response

#model to use: gemini-2.5-flash
##instance = Gemini("gemini-2.5-flash")
##response = instance.generate_response("how are you doing?")
##print(response)


