import random
import requests
from bs4 import BeautifulSoup
import yaml
import os


with open("config.yml", "r") as cfgfile:
    cfg = yaml.safe_load(cfgfile)


address = cfg['source']['address']
output_folder = cfg['output']['folder_name']

resource = requests.get(address, headers={'user-agent': 'Mozilla/5.0'}).content
resource_html = BeautifulSoup(resource, "lxml")
resource_title = resource_html.select('title')[0].get_text() + ".html"
resource_images = resource_html.findAll('img')
resource_styles = resource_html.select('[rel="stylesheet"]')  # list


def delete_output_folder(output_folder):
    try:
        if(os.listdir(output_folder)):
            remaining_files = os.listdir(output_folder)
            if(len(remaining_files) > 0):
                for file in remaining_files:
                    # Remove images inside images folder
                    for image in os.listdir(os.path.join(output_folder, file)):
                        os.remove(os.path.join(output_folder, 'images', image))
                    # Remove Files
                    if(len(os.listdir(os.path.join(output_folder, file))) > 0):
                        os.remove(os.path.join(output_folder, file))
                    # Remove Folders
                    os.rmdir(os.path.join(output_folder, file))
        # Remove output folder
        os.rmdir(output_folder)

    except:
        pass


def folder_init(output_folder):
    os.mkdir(output_folder)
    os.chdir(output_folder)
    os.mkdir("images")


def scrape_html(output_folder):
    with open((os.path.join(os.getcwd(),  resource_title)), 'w', encoding="utf-8") as html:
        html.write(resource_html.prettify())


def scrape_images(output_folder):
    formats = ['.jpg', '.png', '.svg']
    for format in formats:
        for number, image in enumerate(resource_images):
            if image['src'].endswith(format):
                if not image['src'].startswith("/static"):
                    with open((os.path.join(os.getcwd(), 'images', f"image{random.randint(0,10000000000)}{format}")), 'wb') as img:
                        img.write(requests.get(
                            f'https:{image["src"]}').content)


if __name__ == "__main__":
    delete_output_folder(output_folder)
    folder_init(output_folder)
    scrape_html(output_folder)
    scrape_images(output_folder)
