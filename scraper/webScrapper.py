import requests
from PIL import Image
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, "html.parser")

    def get_title(self):
        h1 = self.soup.find('h1').text
        return h1

    def get_text(self, className):
        parragraph = self.soup.find('div', {'class': className}).find_all('p')
        return parragraph

    def get_image(self, className):
        image_path = className + ".png"
        section_intent = self.soup.find('div', {'class': className})
        figure_tag = section_intent.find('figure')
        image_url = "http://refactoring.guru" + figure_tag.find('img')['src']
        image_data = requests.get(image_url)
        try:
            image_data.raise_for_status()  # Check if the image was retrieved successfully
        except requests.exceptions.HTTPError:
            print("Could not retrieve image")
            return None
        with open(image_path, 'wb') as f:
            f.write(image_data.content)
        original_image = Image.open(image_path)
        if original_image.mode != 'RGBA':
            original_image = original_image.convert('RGBA')
        new_image = Image.new('RGBA', original_image.size, (255, 255, 255, 255))
        new_image.paste(original_image, (0, 0), original_image)
        new_image.save(image_path)
        return image_path

