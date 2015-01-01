"""
    Download Manager
    (c) 2015 Roy Portas
"""

from requests import get, head, codes
from hashlib import md5
from re import findall
from os import remove, path
from PySide import QtGui, QtCore
import sys
import threading

from main import Ui_MainWindow as mainFrame
from popup import Ui_Dialog as popupFrame


class Popup(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.ui = popupFrame()
        self.ui.setupUi(self)
        self.show()
        
    def accept(self):
        #self.parent.downloads.append()
        url = self.ui.urlEdit.text()
        filename = self.ui.filenameEdit.text()
        md5 = self.ui.hashEdit.text()
        self.parent.downloads.append(Download(url, filename, md5))
        self.parent.updateTable()
        self.close()
        
    def reject(self):
        self.close()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainFrame()
        self.ui.setupUi(self)
        
        self.downloads = []
        self.popup = None

        self.ui.actionNew_Download.triggered.connect(self.addDownload)
        self.ui.startButton.clicked.connect(self.startDownload)
        self.ui.stopDownload.clicked.connect(self.stopDownload)
        self.ui.pauseButton.clicked.connect(self.pauseDownload)
        self.show()
        
    def addDownload(self):
        self.popup = Popup(self)
        
    def updateTable(self):
        self.ui.downloadsList.clear()
        for download in self.downloads:
            self.ui.downloadsList.addItem(str(download))
        
    def startDownload(self):
        index = self.ui.downloadsList.currentRow()
        if index != -1:
            self.downloads[index].parentWindow = self
            self.downloads[index].startDownload()
            
    def stopDownload(self):
        index = self.ui.downloadsList.currentRow()
        if index != -1:
            self.downloads[index].stopDownload()
            self.downloads.pop(index)
            self.updateTable()

    def pauseDownload(self):
        index = self.ui.downloadsList.currentRow()
        if index != -1:
            self.downloads[index].pauseDownload()


class Download:
    def __init__(self, url, filename, md5hash):
        self.url = url
        self.filename = filename
        self.md5hash = md5hash
        self.progress = 0
        self.thread = None
        self.parentWindow = None
        self.downloadActive = 0

    def setProgress(self, progress):
        try:
            self.progress = progress
            self.parentWindow.updateTable()
        except:
            pass
            # PLEASE FIX MY ERROR PYTHON GODS

    def startDownload(self):
        if self.filename == "":
            self.filename = None
        """
        self.thread = threading.Thread(target=downloadFile, args=(self.url,
                                                             self.parentWindow,
                                                             self.filename,
                                                             self.md5hash,
                                                             self))
        """
        self.thread = DownloadThread()
        self.thread.setData(self.url, self.filename, self.md5hash, self)
        self.thread.start()
        self.downloadActive = 1
    
    def pauseDownload(self):
        if self.downloadActive == 1:
            self.downloadActive = 0
            print("Disabled download")
        else:
            self.downloadActive = 1
            print("Activated download")
    
    def stopDownload(self):
        print("Stopping download")

    def __str__(self):
        if self.filename == "":
            return "{} - {}".format(self.url, self.progress)
        else:
            return "{} - {}".format(self.filename, self.progress)

#TODO: Move this into a QT Thread and pass the listWidget into it
# Example: http://stackoverflow.com/questions/9957195/updating-gui-elements-in-multithreaded-pyqt


class DownloadThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.url = None
        self.filename = None
        self.md5hash = None

    def setData(self, url, filename, md5hash, parent):
        self.parent = parent
        self.url = url
        self.filename = filename
        self.md5hash = md5hash

    def run(self):
        self.startDownload()
        self.exec_()

    def startDownload(self):
        try:
            amount = 1024
            headers = head(self.url).headers
            filesize = headers.get("Content-Length")
            if self.filename == None:
                # Automatically name the file
                content = headers.get('content-disposition')
                dlFilename = findall('filename="(.*)"', content)[0]
                self.filename = dlFilename
                self.parent.filename = self.filename
                self.parent.setProgress(0)

            if path.isfile(self.filename):
                remove(self.filename)

            offset = 0

            with open(self.filename, 'wb') as f:
                req = get(self.url, stream=True)
                if req.status_code == codes.ok:
                    print("Status code OK, proceeding with download")
                    recSize = 0
                    print("Starting download")
                    for chunk in req.iter_content(amount):
                        recSize += amount
                        if filesize:
                            print("Received {}/{}".format(recSize, filesize))
                            prog = float(recSize)/float(filesize)
                            self.parent.setProgress("{}%".format(prog))
                        else:
                            print("Received {}".format(recSize))
                            dlText = "Downloaded {}mb".format(float(recSize)/float(1000000))

                            offset += 1

                            if offset > 10:
                                self.parent.setProgress(dlText)
                                offset = 0

                        f.write(chunk)

                    print("Download finished")
                    self.parent.setProgress("Download Complete")

                else:
                    print("Bad status code received, canceling download [Status code: {}]".format(req.status_code))

        except Exception as e:
            print("ERROR: {}".format(e))


def downloadFile(url, parentWindow, filename=None, md5hash=None, parent=None):
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
            parent.filename = filename
            parentWindow.updateTable()
            
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
                        prog = float(recSize)/float(filesize)
                        parent.progress = prog * 100
                        parentWindow.updateTable()
                    else:
                        print("Received {}".format(recSize))
                        dlText = "Downloaded {}mb".format(float(recSize)/float(1000000))
                        parent.progress = dlText
                        parentWindow.updateTable()

                    f.write(chunk)
                    while parent.downloadActive == 0:
                        pass
                print("Download finished")
                #parent.progress = "Download Complete"
                #parentWindow.updateTable()
                
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
        fhash = md5(f.read()).hexdigest()
        if fhash == md5sum:
            return True
        else:
            return False

#downloadFile("http://downloads.sourceforge.net/project/filezilla/FileZilla_Client/3.9.0.6/FileZilla_3.9.0.6_x86_64-linux-gnu.tar.bz2?r=&ts=1419810214&use_mirror=softlayer-sng", None, "07f9fa2a5069932285e0217bfd350626")


def main():
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()