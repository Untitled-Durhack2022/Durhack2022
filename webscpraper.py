from io import BytesIO
import pycurl
import certifi
from bs4 import BeautifulSoup

class httpWebpage:
    def __init__(self):
        self.body = None
        self.head = None


## Syncrhonous Scraper
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
        webpage.head = webpage.head.getvalue()
        webpage.body = BeautifulSoup(webpage.body.getvalue(), "lxml")
        return webpage


    def scrapeZoopla(self, term):
        url = f"https://www.zoopla.co.uk/for-sale/property/county-durham/?q=county%20durham&results_sort=newest_listings&search_source=for-sale"
        counter = 1
        while True:
            newurl = f"{url}&pn={counter}"
            filename = f"output\\{term}{counter}.txt"
            print(newurl)

            resp = self.makeRequest(newurl)
            webpage = self.parseHttpPage(resp)
            if webpage.body.find("div", {"content": "No results found"}) != None: break

            with open(filename, "w+") as outfile:
                outfile.write(str(webpage.body))
            counter += 1


        print("exiting")

        



def main():
    s = scraper()
    # s.scrapeZoopla("county_durham")

    d = dataprocessor()


if __name__ == "__main__":
    main()


