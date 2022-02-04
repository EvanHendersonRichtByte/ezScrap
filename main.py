import random
import requests
import yaml
import os
import pdb
from bs4 import BeautifulSoup

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
        list_dir = os.listdir(output_folder)
        if len(list_dir) != 0:
            # Remove images inside images folder
            if 'images' in list_dir:
                for image in os.listdir(os.path.join(output_folder, 'images')):
                    os.remove(os.path.join(
                        output_folder, 'images', image))
                os.rmdir(os.path.join(output_folder, 'images'))
            if 'css' in list_dir:
                for css in os.listdir(os.path.join(output_folder, 'css')):
                    os.remove(os.path.join(
                        output_folder, 'css', css))
                os.rmdir(os.path.join(output_folder, 'css'))

        # Remove Files
        for file in list_dir:
            os.remove(os.path.join(output_folder, file))
        # Remove output folder
        os.rmdir(output_folder)
    except:
        print("Please re-run the program")


def folder_init(output_folder):
    if not output_folder in os.listdir(os.getcwd()):
        os.mkdir(output_folder)
        os.makedirs(os.path.join(output_folder, 'images'))
        os.makedirs(os.path.join(output_folder, 'css'))
        scrape_html(output_folder)
        scrape_css(output_folder)
        scrape_images(output_folder)


def scrape_html(output_folder):
    output_folder = os.path.join(os.getcwd(), output_folder, resource_title)
    with open(output_folder, 'w', encoding="utf-8") as html:
        html.write(resource_html.prettify())


def scrape_css(output_folder):
    for style in resource_styles:
        with open((os.path.join(os.getcwd(), output_folder, 'css', f"css{random.randint(0,10000000000)}.css")), 'w') as css:
            css.write(str(requests.get(
                "https://wikipedia.org" + style['href']).content))


def scrape_images(output_folder):
    formats = ['.jpg', '.png', '.svg']
    for format in formats:
        for number, image in enumerate(resource_images):
            if image['src'].endswith(format):
                if not image['src'].startswith("/static"):
                    with open((os.path.join(os.getcwd(), output_folder, 'images', f"image{random.randint(0,10000000000)}{format}")), 'wb') as img:
                        img.write(requests.get(
                            f'https:{image["src"]}').content)


if __name__ == "__main__":
    delete_output_folder(output_folder)
    folder_init(output_folder)
