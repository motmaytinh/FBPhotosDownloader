"""FB Photos Downloader"""

import urllib
import json
import os

ACESS_TOKEN = "902628199904076|PEW80o6zhsRTEQlwLSZ0ZTphUw4"
ALBUM_PARAM_URL = "https://graph.facebook.com/{PAGE_ID}/albums?fields=count,name,description&access_token={TOKEN}"
PHOTOS_PARAM_URL = "https://graph.facebook.com/v2.11/{ALBUM_ID}/photos/uploaded?limit=40&access_token={TOKEN}"
PHOTO_URL = "https://graph.facebook.com/v2.11/{PHOTOS_ID}?fields=images&access_token={TOKEN}"
FILE_NAME = "log.txt"

def album_list_getter(in_page_id):
    """Return list of albums of page"""

    album_node_url = ALBUM_PARAM_URL.format(PAGE_ID=in_page_id, TOKEN=ACESS_TOKEN)
    return_album_node = urllib.urlopen(album_node_url)
    album_node = json.loads(return_album_node.read())
    return album_node['data']

def print_album_list(album_list):
    """Print album list and return the album name choice.

    If return is all then all photos on page will be download."""

    for i in range(len(album_list)):
        print "{}. {} ({} photo(s))".format(i + 1, album_list[i]['name'], album_list[i]['count'])

    choice = raw_input("Please enter your choice (0 for all): ")
    return int(choice) - 1

def get_photo_list(album_url):
    """Return list of photo in album"""

    return_album = urllib.urlopen(album_url)
    album_data = json.loads(return_album.read())
    try:
        return album_data['data'], album_data['paging']['next']
    except Exception:
        return album_data['data'], ''
    

def download_photos(album_name, album_id, file_name):
    """Download photos and save to folder."""

    photo_list, next_pointer = get_photo_list(PHOTOS_PARAM_URL.format(ALBUM_ID=album_id, TOKEN=ACESS_TOKEN))

    newpath = "./" + album_name
    if not os.path.exists(newpath):
        os.makedirs(newpath, mode=0o777)

    downloaded = set([])
    log_file_path = newpath + '/' + FILE_NAME
    check = False
    if os.path.exists(log_file_path):
        check = True
        log = open(log_file_path, 'r+')
        for line in log:
            downloaded.add(int(line))
    else:
        log = open(log_file_path, 'w')

    count = 0
    while True:
        for photo in photo_list:
            photo_id = int(photo['id'])
            if check:
                if photo_id in downloaded:
                    print "Photo downloaded"
                    continue
            photo_url = PHOTO_URL.format(PHOTOS_ID=photo_id, TOKEN=ACESS_TOKEN)
            return_photo = urllib.urlopen(photo_url)
            photo_links = json.loads(return_photo.read())
            image_link = photo_links['images'][0]['source']
            urllib.urlretrieve(image_link, '{}/{} {}.jpg'.format(newpath, file_name, count))
            log.write(photo['id'] + '\n')
            count += 1
            print '{} photo(s) downloaded.'.format(count)
        if next_pointer == '':
            break
        else:
            photo_list, next_pointer = get_photo_list(next_pointer)


    log.close()
    os.remove(log_file_path)

    return

def main():
    """Program starting point"""

    while True:
        choice = raw_input("Do you have a (p)age ID or (a)lbum ID: ")
        if choice in ('p', 'P'):
            page_id = raw_input("Please enter a page id: ")
            album_list = album_list_getter(page_id)
            index = print_album_list(album_list)
            if index == -1:
                download_photos(page_id, page_id, page_id)
            else:
                download_photos(album_list[index]['name'], album_list[index]['id'], album_list[index]['name'])
            break
        elif choice in ('a', 'A'):
            album_id = raw_input("Please enter an album id: ")
            download_photos('name', album_id, 'Gai xinh')
            break

    print 'Done'

main()
