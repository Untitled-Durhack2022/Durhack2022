from io import BytesIO
import pycurl
import certifi
from bs4 import BeautifulSoup

class httpWebpage:
    def __init__(self):
        self.body = None
        self.head = None


class scraper:
    def __init__(self):
        bufferData = BytesIO()
        bufferHeader = BytesIO()

        c = pycurl.Curl()
        c.setopt(c.CAINFO, certifi.where())
        ##The writedate and writeheader should be local, therefore we can't have them here
        c.setopt(c.WRITEDATA, bufferData)
        c.setopt(c.WRITEHEADER, bufferHeader)
        c.setopt(c.FOLLOWLOCATION, True)
        c.setopt(c.ACCEPT_ENCODING, "*")

        self.curlHandle = c


    def makeRequest(self, encodedURL, customHTTPHeaders=[]):
        currentHandle = self.curlHandle
        
        ##Now that we have a currentHandle, we can work with it 
        currentHandle.setopt(currentHandle.URL, encodedURL)
        currentHandle.setopt(currentHandle.HTTPHEADER, customHTTPHeaders)

        bufferData = BytesIO()
        bufferHeader = BytesIO()
        
        currentHandle.setopt(currentHandle.WRITEDATA, bufferData)
        currentHandle.setopt(currentHandle.WRITEHEADER, bufferHeader)

        currentHandle.perform()

        webpage = httpWebpage()
        webpage.body = bufferData
        webpage.head = bufferHeader
        return webpage


    def parseHttpPage(self, webpage):
        webpage.body = webpage.body.getvalue()
        webpage.head = webpage.head.getvalue()
        return webpage


def main():
    s = scraper()
    ret = s.makeRequest("https://www.google.com")
    webpage = s.parseHttpPage(ret)


if __name__ == "__main__":
    main()


