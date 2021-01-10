from os.path import join
import spiders
from urllib.parse import urlparse

def download_book(url, output):
    url_info = urlparse(url)
    host = url_info.hostname
    spdier = spiders.SpdierSupportList[host]
    if spdier == None:
        print('No support %s yet' % host)
        return
    spdier.load(url,output)
