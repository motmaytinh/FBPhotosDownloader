"""FB Photos Downloader"""

import urllib
import json
import os
import stat

ACESS_TOKEN = "902628199904076|PEW80o6zhsRTEQlwLSZ0ZTphUw4"
ALBUM_PARAM_URL = "https://graph.facebook.com/{PAGE_ID}/albums?fields=count,name,description&access_token={TOKEN}"
PHOTOS_PARAM_URL = "https://graph.facebook.com/{ALBUM_ID}/photos?access_token={TOKEN}"
PHOTO_URL = "https://graph.facebook.com/v2.11/{PHOTOS_ID}?fields=images&access_token={TOKEN}"

def album_list_getter(in_page_id):
    """Return list of albums of page"""

    album_node_url = ALBUM_PARAM_URL.format(PAGE_ID=in_page_id, TOKEN=ACESS_TOKEN)
    #print album_node_url
    return_album_node = urllib.urlopen(album_node_url)
    album_node = json.loads(return_album_node.read())
    return album_node['data']

def print_album_list(album_list):
    """Print album list and return the album name choice.

    If return is all then all photos on page will be download."""

    for i in range(len(album_list)):
        print "{}. {} ({} photo(s))".format(i + 1, album_list[i]['name'], album_list[i]['count'])

    choice = raw_input("Please enter your choice (0 for all): ")
    return -1 if (int(choice) == 0) else int(choice) - 1

def get_photo_list(album_id):
    album_url = PHOTOS_PARAM_URL.format(ALBUM_ID=album_id, TOKEN=ACESS_TOKEN)

    return_album = urllib.urlopen(album_url)
    album_data = json.loads(return_album.read())
    return album_data['data']

def download_photos(album_name, album_id, file_name):
    """Download photos and save to folder."""

    if album_id == "all":
        return

    photo_list = get_photo_list(album_id)

    #newpath = "/img" + album_name
    #if not os.path.exists(newpath):
    #    os.makedirs(newpath, mode=0o777)

    for i in range(len(photo_list)):
        photo_url = PHOTO_URL.format(PHOTOS_ID=photo_list[i]['id'], TOKEN=ACESS_TOKEN)
        return_photo = urllib.urlopen(photo_url)
        photo_links = json.loads(return_photo.read())
        image_link = photo_links['images'][0]['source']
        urllib.urlretrieve(image_link, file_name + str(i) + '.jpg')

    return

def main():
    """Program starting point"""

    while True:
        choice = raw_input("Do you have a page ID or album ID (P/A): ")
        if choice in ('p', 'P'):
            page_id = raw_input("Please enter a page id: ")
            album_list = album_list_getter(page_id)
            index = print_album_list(album_list)
            download_photos(album_list[index]['name'], album_list[index]['id'], album_list[index]['name'])
            break
        elif choice in ('a', 'A'):
            album_id = raw_input("Please enter an album id: ")
            download_photos('name', album_id, 'Gai xinh')
            break

    print 'Done'

main()