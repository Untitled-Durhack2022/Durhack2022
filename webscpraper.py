from io import BytesIO
import pycurl
import certifi
from bs4 import BeautifulSoup
import pandas

from os import listdir
from os.path import isfile, join

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
            filename = f"output\\zoopla\\{term}{counter}.html"
            print(newurl)

            resp = self.makeRequest(newurl)
            webpage = self.parseHttpPage(resp)
            if webpage.body.find("div", {"content": "No results found"}) != None: break

            with open(filename, "w+") as outfile:
                outfile.write(str(webpage.body))
            counter += 1


        print("exiting")

        
class dataprocesser:
    def __init__(self):
        ## These are the svg paths
        self.svgPaths = {
            "bedroom": "M2.288 4.375c0-.69.56-1.25 1.25-1.25h12.924c.69 0 1.25.56 1.25 1.25v3.492a4.074 4.074 0 00-.349-.139A2 2 0 0015.5 5h-3a2 2 0 00-1.937 2.5h-.626A2.004 2.004 0 008 5H4.5a2 2 0 00-1.863 2.728 4.074 4.074 0 00-.349.139V4.375zm-1.5 4.72v-4.72a2.75 2.75 0 012.75-2.75h12.924a2.75 2.75 0 012.75 2.75v4.72c.338.492.538 1.077.538 1.724v.857a.746.746 0 01-.114.397c.225.234.364.552.364.903v2.295a1.3 1.3 0 01-.941 1.25c.433.553.691 1.25.691 2.008h-1.5c0-.974-.789-1.762-1.762-1.762H3.512c-.973 0-1.762.788-1.762 1.762H.25c0-.758.258-1.455.691-2.008A1.3 1.3 0 010 15.27v-2.295c0-.35.139-.669.364-.903a.747.747 0 01-.114-.397v-.857c0-.647.2-1.232.538-1.724zM4.5 6.5H8a.5.5 0 01.03 1H4.47a.5.5 0 01.03-1zm0 2.5h-.499c-1.357 0-2.25.919-2.25 1.82v.856h16.5v-.857c0-.9-.895-1.82-2.25-1.82h-.442L15.5 9h-11zm7.97-1.5h3.06a.5.5 0 00-.03-1h-3a.5.5 0 00-.03 1zM1.5 15.07v-1.894h17v1.895h-17z",
            "reception":"M4.279 4.749A3.101 3.101 0 017.38 1.647h5.24a3.101 3.101 0 013.1 3.103v2.39c.376-.235.82-.37 1.297-.37a2.441 2.441 0 012.446 2.437 2.42 2.42 0 01-.936 1.916v5.069a.574.574 0 01-.244.47 2.77 2.77 0 01.712 1.857h-1.15c0-.9-.73-1.63-1.63-1.63H3.784c-.9 0-1.63.73-1.63 1.63h-1.15c0-.714.27-1.365.712-1.857a.574.574 0 01-.244-.47v-5.069a2.423 2.423 0 01-.936-1.916A2.441 2.441 0 012.982 6.77c.476 0 .92.135 1.297.37V4.75zm.197 9.081a.576.576 0 01-.197-.433m0-2.328V9.2a1.291 1.291 0 00-1.297-1.28c-.718 0-1.296.579-1.296 1.287 0 .475.257.89.646 1.112.18.103.29.293.29.5v4.798h14.756v-4.799c0-.206.11-.396.29-.499.39-.223.646-.637.646-1.112 0-.708-.578-1.287-1.296-1.287-.72 0-1.297.579-1.297 1.287v4.19a.575.575 0 01-.575.576H4.854a.572.572 0 01-.378-.142m10.095-3.336V4.749a1.951 1.951 0 00-1.951-1.952H7.38A1.951 1.951 0 005.43 4.75v5.745h9.142zm0 2.328H5.43v-1.178h9.142v1.178z",
            "bathroom":"M13.017 2.936A3.093 3.093 0 0115.905.95h.708A3.487 3.487 0 0120.1 4.437v7.69a.752.752 0 01-.017.16v1.382c0 1.707-1.009 3.156-2.46 3.886.3.407.479.91.479 1.456h-1.5a.95.95 0 00-.95-.95H5.607a.95.95 0 00-.95.95h-1.5c0-.51.156-.983.422-1.376-1.541-.7-2.628-2.194-2.628-3.966v-2.602c0-.121-.117-.291-.352-.291H.05v-1.5h.549c.982 0 1.852.762 1.852 1.79v.031h16.132v-1.071c0-.054.006-.107.017-.158V4.437c0-1.098-.89-1.987-1.987-1.987h-.708a1.59 1.59 0 00-1.322.706c.55.209 1.058.56 1.466 1.052l.82.989a1.5 1.5 0 01-1.154 2.457h-4.8a1.5 1.5 0 01-1.154-2.457l.82-.99a3.531 3.531 0 012.436-1.271zM2.451 13.669v-1.072h16.132v1.072c0 1.557-1.35 2.892-3.107 2.892H5.558c-1.757 0-3.107-1.335-3.107-2.892zm13.264-7.515h-4.8l.82-.988c.182-.22.397-.39.632-.512a2.062 2.062 0 011.896 0c.235.122.45.293.632.512l.82.988z"
        }

    def parseZooplaData(self):
        mypath = ".\\output\\"
        files = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]
        properties = []

    
        for filename in files:
            print(filename)
            with open(filename, "r") as infile:
                page = infile.read()

            page = BeautifulSoup(page)
            pagePropertiesDivs = page.findAll("div", {"class" : "css-c3gumt-StyledWrapper e2uk8e30"})
            
            for pageProperty in pagePropertiesDivs:
                textContent = pageProperty.find("div", {"class", "css-mww4lt-StyledContent e2uk8e21"})
                if textContent == None: break

                ## Here we find bedroom, reception, bathroom
                property = {}
                for attribute, path in self.svgPaths.items():
                    ret = textContent.find("path", {"d": path})
                    if ret == None:
                        property[attribute] = None
                    else:
                        property[attribute] = ret.parent.parent.parent["content"]

                ## Here we find the price
                price = textContent.find("p", {"class": "css-1o565rw-Text eczcs4p0"})
                price = price.text[1:].replace(",", "")
                property["price"] = price

                ## Here we find the address
                address = textContent.find("p", {"class": "css-nwapgq-Text eczcs4p0"})
                address = address.text
                property["address"] = address

                properties.append(property)

        df = pandas.DataFrame(properties)
        df.to_csv("data.csv")
        print(df.columns)
        print(df.head)



            ##



        
        

def main():
    s = scraper()
    d = dataprocesser()
    d.parseZooplaData()
    # s.scrapeZoopla("county_durham")



if __name__ == "__main__":
    main()


