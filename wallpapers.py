import os
from configparser import ConfigParser

import requests as rq
from bs4 import BeautifulSoup as BS
from slugify import slugify


def backup(home_path, backup_folder):
    file_names = [x for x in os.listdir(home_path)
                  if os.path.isfile(
                     os.path.join(home_path, x)
                  )]

    backup_path = os.path.join(home_path, backup_folder)

    if not os.path.exists(backup_path):
        os.mkdir(backup_path)

    for f in file_names:
        source_path = os.path.join(home_path, f)
        target_path = os.path.join(home_path, backup_folder, f)
        os.rename(source_path, target_path)


def get_latest_article(uri):
    response = rq.get(uri)

    soup = BS(response.text, 'lxml')

    return soup.select('article a')[0]['href']


def images(uri, target_path):
    response = rq.get(uri)

    soup = BS(response.text, 'lxml')

    uls = soup.select('figure + ul')
    
    for ul in uls:
        image_link = ul.select('li')[1].select('> a')[-1]

        href = image_link['href']

        title = image_link['title']

        print('Downloading %s' % title, end=' ')

        final_path = os.path.join(target_path, slugify(title) + '.jpg')

        print('as %s' % final_path)

        with open(final_path, 'wb') as f:
            f.write(rq.get(href).content)


if __name__ == '__main__':

    CONFIG = ConfigParser()
    CONFIG.read('config.ini')
    WALLPAPERS_HOME = CONFIG['DEFAULT']['wallpapers_home']
    BACKUP_FOLDER   = CONFIG['DEFAULT']['backup_folder']
    URI             = CONFIG['DEFAULT']['uri']

    backup(WALLPAPERS_HOME, BACKUP_FOLDER)
    images(get_latest_article(URI), WALLPAPERS_HOME)

