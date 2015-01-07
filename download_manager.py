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
import Queue
from main import Ui_MainWindow as mainFrame
from popup import Ui_Dialog as popupFrame


class Popup(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.path = ""
        self.ui = popupFrame()
        self.ui.setupUi(self)
        self.ui.downloadPathButton.clicked.connect(self.getPath)
        self.show()

    def getPath(self):
        fpath = QtGui.QFileDialog.getExistingDirectory(self, "Select directory")
        self.ui.filepathDisplay.setText(fpath)
        self.path = fpath

    def accept(self):
        url = self.ui.urlEdit.text()
        filename = self.ui.filenameEdit.text()
        md5 = self.ui.hashEdit.text()
        self.parent.downloads.append(Download(url, filename, md5, self.path))
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
            if self.downloads[index].downloadActive == 0:
                self.downloads[index].parentWindow = self
                self.downloads[index].startDownload()
            
    def stopDownload(self):
        index = self.ui.downloadsList.currentRow()
        if index != -1:
            self.downloads[index].stopDownload()
            self.downloads.pop(index)
            self.updateTable()


class Download:
    def __init__(self, url, filename, md5hash, fpath):
        self.url = url
        self.filename = filename
        self.md5hash = md5hash
        self.path = fpath
        self.progress = 0
        self.thread = None
        self.queue = Queue.Queue()
        self.parentWindow = None
        self.downloadActive = 0
        self.msgBox = None

    def updateProgress(self):
        self.progress = self.queue.get()
        self.parentWindow.updateTable()

    def startDownload(self):
        self.thread = DownloadThread()
        if self.filename == '':
            self.filename = None
        self.thread.setData(self.url, self.filename, self.path, self.md5hash, self.queue, self)
        self.thread.start()
        self.downloadActive = 1
        #TODO: Disable the button once pressed
    
    def stopDownload(self):
        print("Stopping download")

    def __str__(self):
        if self.filename == "":
            return "{} - {}".format(self.url, self.progress)
        else:
            return "{} - {}".format(self.filename, self.progress)

#TODO: implement a Queue here to parse the data back to the main window
class DownloadThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.queue = None
        self.parent = parent
        self.url = None
        self.filename = None
        self.filepath = None
        self.md5hash = None

    def setData(self, url, filename, filepath, md5hash, queue, parent):
        self.queue = queue
        self.parent = parent
        self.url = url
        self.filepath = filepath
        self.filename = filename
        self.md5hash = md5hash

    def run(self):
        self.startDownload()
        self.exec_()

    def startDownload(self):
        #TODO: Put a try except statement around this once tested
        amount = 1024
        headers = head(self.url).headers
        filesize = headers.get("Content-Length")
        if self.filename == None:
            # Automatically name the file
            content = headers.get('content-disposition')
            if content:
                dlFilename = findall('filename="(.*)"', content)[0]
                self.filename = dlFilename
                self.parent.filename = self.filename
                self.queue.put('0')
                self.parent.updateProgress()
            else:
                self.filename = getFilename(self.url)

                if self.filename == None:
                    self.msgBox = QtGui.QMessageBox()
                    self.msgBox.setText("Cannot determine file name")
                    self.msgBox.exec_()
                    return

                else:
                    self.parent.filename = self.filename
                    self.queue.put('0')
                    self.parent.updateProgress()

        finalPath = path.join(self.filepath, self.filename)

        if path.isfile(finalPath):
            remove(finalPath)

        offset = 0

        with open(finalPath, 'wb') as f:
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

                        offset += 1
                        if offset > 10:

                            self.queue.put("{0:.2f}%".format(prog*100))
                            self.parent.updateProgress()
                            offset = 0
                    else:
                        print("Received {}".format(recSize))
                        dlText = "Downloaded {0:.2f}mb".format(float(recSize)/float(1000000))

                        offset += 1

                        if offset > 10:
                            self.queue.put(dlText)
                            self.parent.updateProgress()
                            offset = 0

                    f.write(chunk)

                print("Download finished")
                self.queue.put("Download Finished")
                self.parent.updateProgress()

                if self.md5hash:
                    if checksum(finalPath, self.md5hash):
                        self.queue.put("Checksum matched")
                        self.parent.updateProgress()
                    else:
                        self.queue.put("Checksum math failed")
                        self.parent.updateProgress()

            else:
                print("Bad status code received, canceling download [Status code: {}]".format(req.status_code))


def checksum(filename, md5sum):
    """Checks the file against the checksum"""
    with open(filename, 'rb') as f:
        fhash = md5(f.read()).hexdigest()
        print("File hash: " + fhash)
        print("MD5 hash: " + md5sum)
        if fhash == md5sum:
            return True
        else:
            return False


def getFilename(url):
    """Attempts to get the filename from the URL"""
    components = url.split('/')
    fname = components[-1]
    if '.' in fname:
        return fname
    else:
        return None


def main():
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()