"""
    Download Manager
    (c) 2015 Roy Portas
"""

from requests import get, head, codes
from hashlib import md5
from re import findall
from os import remove, path

def downloadFile(url, filename=None, md5hash=None):
    """Downloads a file"""
    try:
        amount = 1024
        headers = head(url).headers
        filesize = headers.get('Content-Length')
        if filename == None:
            # Automatically name the file
            content = headers.get('content-disposition')
            dlFilename = findall('filename="(.*)"', content)[0]
            filename = dlFilename
            
        if path.isfile(filename):
            remove(filename)
            
        with open(filename, 'wb') as f:
            req = get(url, stream=True)
            if req.status_code == codes.ok:
                print("Status code OK, proceeding with download")
                recSize = 0
                print("Starting download")
                for chunk in req.iter_content(amount):
                    recSize += amount
                    if filesize:
                        print("Received {}/{}".format(recSize, filesize))
                    else:
                        print("Received {}".format(recSize))
                    f.write(chunk)
                print("Download finished")
                
            else:
                print("Bad status code received, canceling download [Status code: {}]".format(req.status_code))
        
        if md5hash:
            print("Checking checksum")
            if checksum(filename, md5hash):
                print("Checksum matched")
    
    except Exception as e:
        print(e)

def checksum(filename, md5sum):
    """Checks the file against the checksum"""
    with open(filename, 'rb') as f:
        hash = md5(f.read()).hexdigest()
        if hash == md5sum:
            return True
        else:
            return False

downloadFile("http://downloads.sourceforge.net/project/filezilla/FileZilla_Client/3.9.0.6/FileZilla_3.9.0.6_x86_64-linux-gnu.tar.bz2?r=&ts=1419810214&use_mirror=softlayer-sng", None, "07f9fa2a5069932285e0217bfd350626")