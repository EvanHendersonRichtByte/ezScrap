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
resource_styles = resource_html.select('[rel="stylesheet"]')  # list


def delete_output_folder(output_folder):
    try:
        if(os.listdir(output_folder)):
            remaining_files = os.listdir(output_folder)
            if(len(remaining_files) > 0):
                for file in remaining_files:
                    os.remove(os.path.join(output_folder, file))
            os.rmdir(output_folder)
    except:
        print("There is no files in output folder")

delete_output_folder(output_folder)

os.mkdir(output_folder)
output_folder = os.path.join(os.getcwd(), output_folder)
with open((os.path.join(output_folder, resource_title)), 'w', encoding="utf-8") as html:
    html.write(resource_html.prettify())

# a = open(f'./output/a.html', 'w+')
# resource_scripts = resource.select('[rel="stylesheet"]')
