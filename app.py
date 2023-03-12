import openai
import requests
from datetime import datetime
import argparse
import os
import subprocess

class OpenAI:
    def __init__(self, user_name, api_token, image_text):
        self.user_name = user_name
        self.api_token = api_token
        self.image_text = image_text        

    def requestImageURL(self):
        response = openai.Image.create(
        prompt= self.image_text,
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url
    
    def downloadImageFromURL(self, image_url):
        file_name = self.user_name + ' ' + self.image_text + ' ' + self.getTimestamp()
        file_name = file_name.lower().strip().replace(' ', '_') + '.jpg'
        response = requests.get(image_url)
        result_image_path = os.getcwd() + os.sep + 'output_images' + os.sep + file_name
        with open(result_image_path, "wb") as fp:
            fp.write(response.content)
        print('Image downloaded: ' + result_image_path)
        subprocess.call(['open', result_image_path])

    def getTimestamp(self):
        return str(datetime.now()).replace(' ', '').replace(':', '').replace('-', '').replace('.', '')
    
    def main(self):
        openai.api_key = self.api_token
        url = self.requestImageURL()
        self.downloadImageFromURL(url)

    
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user_name", help = "User Name")
    parser.add_argument("-i", "--image_text", help = "Text to generate image")
    parser.add_argument("-t", "--api_token", help = "API Token")
    args = parser.parse_args()
    openai_object = OpenAI(args.user_name, args.api_token, args.image_text)
    openai_object.main()
    
    