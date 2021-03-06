import requests
from bs4 import BeautifulSoup
import pandas

l = []

base_url = "http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s="

r = requests.get(base_url)
c = r.content
soup = BeautifulSoup(c, "html.parser")
page_num = soup.find_all("a", {"class": "Page"})[-1].text
print(page_num)

for page in range(0, int(page_num) * 10, 10):
    print(base_url + str(page))
    r = requests.get(base_url + str(page))
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class": "propertyRow"})

    for item in all:
        d = {}
        d["Address"] = item.find_all("span", {"class": "propAddressCollapse"})[0].text
        d["Locality"] = item.find_all("span", {"class": "propAddressCollapse"})[1].text
        d["Price"] = item.find("h4", {"class": "propPrice"}).text.replace("\n", "").replace(" ", "")

        d["Beds"] = item.find("span", {"class": "infoBed"}).find("b").text if item.find("span", {"class": "infoBed"}) else "None"
        d["Area"] = item.find("span", {"class": "infoSqFt"}).find("b").text if item.find("span", {"class": "infoSqFt"}) else "None"
        d["Full Baths"] = item.find("span", {"class": "infoValueFullBath"}).find("b").text if item.find("span", {"class": "infoValueFullBath"}) else "None"
        d["Half Baths"] = item.find("span", {"class": "infoValueHalfBath"}).find("b").text if item.find("span", {"class": "infoValueHalfBath"}) else "None"

        for column_group in item.find_all("div", {"class": "columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class": "featureGroup"}), column_group.find_all("span", {"class": "featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text
        l.append(d)

df = pandas.DataFrame(l)
df.to_csv("estate.csv")
