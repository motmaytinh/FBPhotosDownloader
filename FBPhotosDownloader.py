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

def download_photos(album_name, album_id, file_name):
    album_url = ""

    if album_id == "all":
        return
    else:
        album_url = PHOTOS_PARAM_URL.format(ALBUM_ID=album_id, TOKEN=ACESS_TOKEN)

    return_album = urllib.urlopen(album_url)
    album_data = json.loads(return_album.read())
    photo_list = album_data['data']

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

PAGE_NAME = "the.girl.magz"

def main():
    album_list = album_list_getter(PAGE_NAME)
    id = print_album_list(album_list)
    download_photos(album_list[id]['name'], album_list[id]['id'], album_list[id]['name'])

    print 'Done'

main()